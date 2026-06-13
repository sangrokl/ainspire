/**
 * MCP Resources for Adobe Premiere Pro
 *
 * This module provides resources that give AI agents access to contextual
 * information about Adobe Premiere Pro projects, sequences, and media.
 */
import type { PremiereProTransport } from '../bridge/types.js';
export interface MCPResource {
    uri: string;
    name: string;
    description: string;
    mimeType: string;
}
export declare class PremiereProResources {
    private bridge;
    private logger;
    constructor(bridge: PremiereProTransport);
    getAvailableResources(): MCPResource[];
    readResource(uri: string): Promise<any>;
    getResource(uri: string): MCPResource | undefined;
    private getProjectInfo;
    private getProjectSequences;
    private getProjectMedia;
    private getProjectBins;
    private getTimelineClips;
    private getTimelineTracks;
    private getTimelineMarkers;
    private getAvailableEffects;
    private getAppliedEffects;
    private getAvailableTransitions;
    private getExportPresets;
    private getProjectMetadata;
    private getInstructions;
}
//# sourceMappingURL=index.d.ts.map