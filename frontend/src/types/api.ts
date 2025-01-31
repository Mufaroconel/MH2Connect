import { z } from 'zod';

// API Response Schemas
export const StudentSchema = z.object({
  id: z.string(),
  firstName: z.string(),
  lastName: z.string(),
  dateOfBirth: z.string(),
  gender: z.enum(['male', 'female']),
  email: z.string().email(),
  phoneNumber: z.string(),
  address: z.string(),
  previousSchool: z.string(),
  applicationStatus: z.enum(['pending', 'approved', 'rejected']),
  documents: z.object({
    oLevelResults: z.string(),
    birthCertificate: z.string(),
    nationalId: z.string(),
  }),
  submittedAt: z.string(),
});

export const NotificationSchema = z.object({
  id: z.string(),
  message: z.string(),
  type: z.enum(['success', 'error', 'info', 'warning']),
  timestamp: z.string(),
});

// Infer TypeScript types from schemas
export type Student = z.infer<typeof StudentSchema>;
export type Notification = z.infer<typeof NotificationSchema>;