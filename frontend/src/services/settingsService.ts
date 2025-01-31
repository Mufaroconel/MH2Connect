import { apiClient } from './apiClient';

export interface UserSettings {
  id: number;
  username: string;
  email?: string;
  role?: string;
  avatar?: string;
  lastPasswordChange?: string;
  notificationPreferences?: {
    email: boolean;
    system: boolean;
  };
}

export const settingsService = {
  getUserSettings: async (): Promise<UserSettings> => {
    return await apiClient.get('/api/settings/user');
  },

  updateUserSettings: async (data: Partial<UserSettings>): Promise<UserSettings> => {
    return await apiClient.put('/api/settings/user', data);
  },

  updatePassword: async (data: { currentPassword: string; newPassword: string }): Promise<void> => {
    return await apiClient.put('/api/settings/password', data);
  },

  updateNotificationPreferences: async (preferences: { email: boolean; system: boolean }): Promise<void> => {
    return await apiClient.put('/api/settings/notifications', preferences);
  }
}; 