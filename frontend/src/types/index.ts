export interface VideoMetadata {
  video_id: string;
  platform: "youtube" | "instagram";
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
  transcript?: string;
}

export interface Source {
  video_id: string;
  platform: string;
  creator: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}