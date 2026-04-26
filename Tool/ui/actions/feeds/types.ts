// Scan notification type definitions

export const SCAN_NOTIFICATION_STATE = {
  COMPLETED: "completed",
  FAILED: "failed",
  CANCELLED: "cancelled",
} as const;

export type ScanNotificationState =
  (typeof SCAN_NOTIFICATION_STATE)[keyof typeof SCAN_NOTIFICATION_STATE];

export interface ScanNotification {
  id: string;
  name?: string;
  state: ScanNotificationState;
  progress: number;
  duration: number;
  startedAt: string | null;
  completedAt: string | null;
  trigger: "manual" | "scheduled";
  providerType?: string;
  providerAlias?: string;
  providerUid?: string;
}

export interface ScanNotificationsData {
  items: ScanNotification[];
  totalCount: number;
}

export interface ScanNotificationError {
  message: string;
}
