export interface VideoMetadata {
  video_id: string;
  platform: string;
  title: string;
  creator: string;
  views: number;
  likes: number;
  comments: number;
  followers?: number;
  hashtags: string[];
  upload_date?: string;
  duration?: number;
  engagement_rate: number;
}

export interface Source {
  video_id: string;
  platform: string;
  creator: string;
  chunk_id: number;
  source: string;
}