/**
 * Bridge module for communicating with Adobe Premiere Pro
 *
 * This module handles the communication between the MCP server and Adobe Premiere Pro
 * using various methods including UXP, ExtendScript, and file-based communication.
 */
import { Logger } from '../utils/logger.js';
import { promises as fs } from 'fs';
import { join } from 'path';
import { v4 as uuidv4 } from 'uuid';
import { createSecureTempDir, validateFilePath } from '../utils/security.js';
const EXTENDSCRIPT_HELPERS = `
function __mcpEscapeString(value) {
  return String(value)
    .replace(/\\\\/g, '\\\\\\\\')
    .replace(/"/g, '\\\\"')
    .replace(/\\r/g, '\\\\r')
    .replace(/\\n/g, '\\\\n')
    .replace(/\\t/g, '\\\\t');
}
function __mcpStringify(value) {
  if (value === null) return 'null';
  var valueType = typeof value;
  if (valueType === 'string') return '"' + __mcpEscapeString(value) + '"';
  if (valueType === 'number') return isFinite(value) ? String(value) : 'null';
  if (valueType === 'boolean') return value ? 'true' : 'false';
  if (value instanceof Array) {
    var arrayParts = [];
    for (var i = 0; i < value.length; i++) {
      arrayParts.push(__mcpStringify(value[i]));
    }
    return '[' + arrayParts.join(',') + ']';
  }
  if (valueType === 'object') {
    var objectParts = [];
    for (var key in value) {
      if (value.hasOwnProperty && !value.hasOwnProperty(key)) continue;
      if (typeof value[key] === 'undefined' || typeof value[key] === 'function') continue;
      objectParts.push(__mcpStringify(String(key)) + ':' + __mcpStringify(value[key]));
    }
    return '{' + objectParts.join(',') + '}';
  }
  return 'null';
}
if (typeof JSON === 'undefined') { JSON = {}; }
if (typeof JSON.stringify !== 'function') { JSON.stringify = __mcpStringify; }
function __findSequence(id) {
  for (var i = 0; i < app.project.sequences.numSequences; i++) {
    if (app.project.sequences[i].sequenceID === id) return app.project.sequences[i];
  }
  return null;
}
function __findClip(nodeId) {
  var seq = app.project.activeSequence;
  if (!seq) return null;
  for (var t = 0; t < seq.videoTracks.numTracks; t++) {
    var track = seq.videoTracks[t];
    for (var c = 0; c < track.clips.numItems; c++) {
      if (track.clips[c].nodeId === nodeId)
        return { clip: track.clips[c], track: track, trackIndex: t, clipIndex: c, trackType: 'video' };
    }
  }
  for (var t = 0; t < seq.audioTracks.numTracks; t++) {
    var track = seq.audioTracks[t];
    for (var c = 0; c < track.clips.numItems; c++) {
      if (track.clips[c].nodeId === nodeId)
        return { clip: track.clips[c], track: track, trackIndex: t, clipIndex: c, trackType: 'audio' };
    }
  }
  return null;
}
function __findProjectItem(nodeId) {
  function walk(item) {
    if (item.nodeId === nodeId) return item;
    if (item.children) {
      for (var i = 0; i < item.children.numItems; i++) {
        var found = walk(item.children[i]);
        if (found) return found;
      }
    }
    return null;
  }
  return walk(app.project.rootItem);
}
function __ticksToSeconds(ticks) {
  return parseInt(ticks, 10) / 254016000000;
}
function __secondsToTicks(seconds) {
  return String(Math.round(seconds * 254016000000));
}
`;
export class PremiereProBridge {
    logger;
    communicationMethod;
    tempDir;
    usesExternalTempDir;
    uxpProcess;
    isInitialized = false;
    sessionId;
    constructor() {
        this.logger = new Logger('PremiereProBridge');
        this.communicationMethod = 'file'; // Default to file-based communication
        this.sessionId = uuidv4();
        // Use PREMIERE_TEMP_DIR if set (same path as UXP plugin "Temp Directory"), else session-specific
        const envDir = process.env.PREMIERE_TEMP_DIR;
        this.usesExternalTempDir = Boolean(envDir);
        this.tempDir = envDir ? envDir.replace(/\/$/, '') : createSecureTempDir(this.sessionId);
    }
    async initialize() {
        try {
            await this.setupTempDirectory();
            await this.detectPremiereProInstallation();
            await this.initializeCommunication();
            this.isInitialized = true;
            this.logger.info('Adobe Premiere Pro bridge initialized successfully');
        }
        catch (error) {
            this.logger.error('Failed to initialize Adobe Premiere Pro bridge:', error);
            throw error;
        }
    }
    async setupTempDirectory() {
        try {
            await fs.mkdir(this.tempDir, { recursive: true, mode: 0o700 }); // Restrict to owner only
            this.logger.debug(`Secure temp directory created: ${this.tempDir}`);
        }
        catch (error) {
            this.logger.error('Failed to create temp directory:', error);
            throw error;
        }
    }
    async detectPremiereProInstallation() {
        // Check for common Premiere Pro installation paths
        const commonPaths = [
            '/Applications/Adobe Premiere Pro 2024/Adobe Premiere Pro 2024.app',
            '/Applications/Adobe Premiere Pro 2023/Adobe Premiere Pro 2023.app',
            'C:\\Program Files\\Adobe\\Adobe Premiere Pro 2024\\Adobe Premiere Pro.exe',
            'C:\\Program Files\\Adobe\\Adobe Premiere Pro 2023\\Adobe Premiere Pro.exe'
        ];
        for (const path of commonPaths) {
            try {
                await fs.access(path);
                this.logger.info(`Found Adobe Premiere Pro at: ${path}`);
                return;
            }
            catch (error) {
                // Continue checking other paths
            }
        }
        this.logger.warn('Adobe Premiere Pro installation not found in common paths');
    }
    async initializeCommunication() {
        // For now, we'll use file-based communication as it's the most reliable
        // In a production environment, you would set up UXP or ExtendScript communication
        this.communicationMethod = 'file';
        this.logger.info(`Using ${this.communicationMethod} communication method`);
    }
    isSelfInvokingScript(script) {
        const trimmed = script.trim();
        return /^\(function\s*\(\)\s*\{[\s\S]*\}\)\s*\(\)\s*;?$/.test(trimmed);
    }
    buildExecutableScript(script) {
        if (this.isSelfInvokingScript(script)) {
            return EXTENDSCRIPT_HELPERS + script.trim();
        }
        // Wrap script bodies so top-level "return ..." remains valid in ExtendScript.
        return EXTENDSCRIPT_HELPERS + '(function(){\n' + script + '\n})();';
    }
    async executeScript(script) {
        if (!this.isInitialized) {
            throw new Error('Bridge not initialized. Call initialize() first.');
        }
        const commandId = uuidv4();
        const commandFile = join(this.tempDir, `command-${commandId}.json`);
        const responseFile = join(this.tempDir, `response-${commandId}.json`);
        try {
            const fullScript = this.buildExecutableScript(script);
            // Write command to file
            await fs.writeFile(commandFile, JSON.stringify({
                id: commandId,
                script: fullScript,
                timestamp: new Date().toISOString()
            }));
            // Wait for response (in a real implementation, this would be handled by the UXP plugin)
            const response = await this.waitForResponse(responseFile);
            // Clean up files
            await fs.unlink(commandFile).catch(() => { });
            await fs.unlink(responseFile).catch(() => { });
            return response;
        }
        catch (error) {
            this.logger.error(`Failed to execute script: ${error}`);
            throw error;
        }
    }
    async waitForResponse(responseFile, timeout = 60000) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeout) {
            try {
                const response = await fs.readFile(responseFile, 'utf8');
                const parsed = JSON.parse(response);
                if (parsed.result !== undefined)
                    return parsed.result;
                return parsed;
            }
            catch (error) {
                await new Promise(resolve => setTimeout(resolve, 150));
            }
        }
        throw new Error('Bridge response timeout. Ensure Premiere Pro is open, MCP Bridge (CEP or UXP) panel is open, ' +
            'Temp Directory is set to ' + this.tempDir + ', and Start Bridge is clicked.');
    }
    // Project Management
    async createProject(name, location) {
        const script = `
      // Create new project
      app.newProject(${JSON.stringify(name)}, ${JSON.stringify(location)});
      var project = app.project;
      
      // Return project info
      return JSON.stringify({
        id: project.documentID,
        name: project.name,
        path: project.path,
        isOpen: true,
        sequences: [],
        projectItems: []
      });
    `;
        return await this.executeScript(script);
    }
    async openProject(path) {
        const script = `
      // Open existing project
      app.openDocument(${JSON.stringify(path)});
      var project = app.project;
      
      // Return project info
      return JSON.stringify({
        id: project.documentID,
        name: project.name,
        path: project.path,
        isOpen: true,
        sequences: [],
        projectItems: []
      });
    `;
        return await this.executeScript(script);
    }
    async saveProject() {
        const script = `
      // Save current project
      app.project.save();
      return JSON.stringify({ success: true });
    `;
        await this.executeScript(script);
    }
    async importMedia(filePath) {
        // Validate file path for security
        const pathValidation = validateFilePath(filePath);
        if (!pathValidation.valid) {
            throw new Error(`Invalid file path: ${pathValidation.error}`);
        }
        // Use the normalized path from validation (don't double-escape)
        const safePath = pathValidation.normalized || filePath;
        const script = `
      try {
        function __walkItems(parent, output) {
          for (var i = 0; i < parent.children.numItems; i++) {
            var child = parent.children[i];
            output.push(child);
            if (child.type === ProjectItemType.BIN) {
              __walkItems(child, output);
            }
          }
        }

        var file = new File(${JSON.stringify(safePath)});
        if (!file.exists) {
          return JSON.stringify({
            success: false,
            error: "File not found: " + ${JSON.stringify(safePath)}
          });
        }

        var existingItems = [];
        __walkItems(app.project.rootItem, existingItems);

        var importResult = app.project.importFiles([file.fsName], true, app.project.rootItem, false);
        if (!importResult) {
          return JSON.stringify({
            success: false,
            error: "Failed to import file"
          });
        }

        var afterItems = [];
        __walkItems(app.project.rootItem, afterItems);

        var importedItem = null;
        for (var j = 0; j < afterItems.length; j++) {
          var candidate = afterItems[j];
          var alreadyPresent = false;
          for (var k = 0; k < existingItems.length; k++) {
            if (existingItems[k].nodeId === candidate.nodeId) {
              alreadyPresent = true;
              break;
            }
          }
          if (alreadyPresent) {
            continue;
          }
          try {
            if (candidate.getMediaPath && candidate.getMediaPath() === file.fsName) {
              importedItem = candidate;
              break;
            }
          } catch (e) {}
          if (!importedItem && candidate.name === file.name) {
            importedItem = candidate;
          }
        }

        if (!importedItem) {
          return JSON.stringify({
            success: false,
            error: "Import completed but imported item could not be located"
          });
        }

        return JSON.stringify({
          success: true,
          id: importedItem.nodeId,
          name: importedItem.name,
          type: importedItem.type.toString(),
          mediaPath: importedItem.getMediaPath ? importedItem.getMediaPath() : file.fsName
        });
      } catch (e) {
        return JSON.stringify({
          success: false,
          error: e.toString()
        });
      }
    `;
        return await this.executeScript(script);
    }
    async createSequence(name, presetPath) {
        const script = `
      // Create new sequence
      var sequence = app.project.createNewSequence(${JSON.stringify(name)}, ${JSON.stringify(presetPath || '')});
      
      // Return sequence info
      return JSON.stringify({
        id: sequence.sequenceID,
        name: sequence.name,
        duration: sequence.end - sequence.zeroPoint,
        frameRate: sequence.framerate,
        videoTracks: [],
        audioTracks: []
      });
    `;
        return await this.executeScript(script);
    }
    async addToTimeline(sequenceId, projectItemId, trackIndex, time) {
        const script = `
      try {
        var sequence = __findSequence(${JSON.stringify(sequenceId)});
        if (!sequence) {
          return JSON.stringify({ success: false, error: "Sequence not found" });
        }

        var projectItem = __findProjectItem(${JSON.stringify(projectItemId)});
        if (!projectItem) {
          return JSON.stringify({ success: false, error: "Project item not found" });
        }

        var track = sequence.videoTracks[${trackIndex}];
        if (!track) {
          return JSON.stringify({ success: false, error: "Video track not found" });
        }

        track.overwriteClip(projectItem, ${time});

        var placedClip = null;
        for (var i = 0; i < track.clips.numItems; i++) {
          var candidate = track.clips[i];
          if (candidate && candidate.projectItem && candidate.projectItem.nodeId === projectItem.nodeId && Math.abs(candidate.start.seconds - ${time}) < 0.1) {
            placedClip = candidate;
            break;
          }
        }

        if (!placedClip && track.clips.numItems > 0) {
          placedClip = track.clips[track.clips.numItems - 1];
        }

        if (!placedClip) {
          return JSON.stringify({ success: false, error: "Clip placement did not produce a track item" });
        }

        return JSON.stringify({
          success: true,
          id: placedClip.nodeId,
          name: placedClip.name,
          inPoint: placedClip.start.seconds,
          outPoint: placedClip.end.seconds,
          duration: placedClip.duration.seconds,
          mediaPath: placedClip.projectItem && placedClip.projectItem.getMediaPath ? placedClip.projectItem.getMediaPath() : ""
        });
      } catch (e) {
        return JSON.stringify({
          success: false,
          error: e.toString()
        });
      }
    `;
        return await this.executeScript(script);
    }
    async renderSequence(sequenceId, outputPath, presetPath) {
        const script = `
      // Render sequence
      var sequence = app.project.getSequenceByID(${JSON.stringify(sequenceId)});
      var encoder = app.encoder;

      encoder.encodeSequence(sequence, ${JSON.stringify(outputPath)}, ${JSON.stringify(presetPath)},
        encoder.ENCODE_ENTIRE, false);

      return JSON.stringify({ success: true });
    `;
        await this.executeScript(script);
    }
    async listProjectItems() {
        const script = `
      try {
        if (!app.project || !app.project.rootItem) {
          throw new Error('No open project');
        }
        function walk(item) {
          var results = [];
          if (item.type === ProjectItemType.BIN) {
            for (var i = 0; i < item.children.numItems; i++) {
              results = results.concat(walk(item.children[i]));
            }
          } else {
            results.push({
              id: item.nodeId || item.treePath || item.name,
              name: item.name,
              type: item.type === ProjectItemType.BIN ? 'bin' : (item.type === ProjectItemType.SEQUENCE ? 'sequence' : 'footage'),
              mediaPath: item.getMediaPath ? item.getMediaPath() : undefined,
              duration: item.getOutPoint ? (item.getOutPoint() - item.getInPoint()) : undefined,
              frameRate: item.getVideoFrameRate ? item.getVideoFrameRate() : undefined
            });
          }
          return results;
        }
        var items = walk(app.project.rootItem);
        return JSON.stringify({ ok: true, items: items });
      } catch (e) {
        return JSON.stringify({ ok: false, error: String(e) });
      }
    `;
        const result = await this.executeScript(script);
        if (result.ok)
            return result.items;
        throw new Error(result.error || 'Unknown error listing project items');
    }
    async cleanup() {
        if (this.uxpProcess) {
            this.uxpProcess.kill();
        }
        // Only remove temp dirs created by this server. The shared bridge directory is
        // configured externally and should persist across restarts.
        try {
            if (!this.usesExternalTempDir) {
                await fs.rm(this.tempDir, { recursive: true });
            }
        }
        catch (error) {
            this.logger.warn('Failed to clean up temp directory:', error);
        }
        this.logger.info('Adobe Premiere Pro bridge cleaned up');
    }
}
//# sourceMappingURL=index.js.map