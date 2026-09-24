export type TankerEvent = {
  id: number;
  camera_id: string;
  site_name: string;
  tracker_id: string;
  state: string;
  entry_time: string | null;
  exit_time: string | null;
  duration_seconds: number | null;
  text_kn: string;
  text_en: string;
  ocr_confidence: number | null;
  snapshot_path: string;
  created_at: string;
  updated_at: string;
};

export type LiveStatus = {
  camera: {
    camera_id: string;
    camera_name: string;
    site_name: string;
    connected: boolean;
    last_frame_at: string | null;
    last_error: string;
  };
  active_tankers: Array<{
    track_id: string;
    bbox: number[];
    confidence: number;
    first_seen_at: string;
    last_seen_at: string;
    stationary_since: string | null;
  }>;
  updated_at: string;
};

