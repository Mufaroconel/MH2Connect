export interface Student {
  id: string;
  firstName: string;
  lastName: string;
  dateOfBirth: string;
  gender: 'male' | 'female';
  email: string;
  phoneNumber: string;
  address: string;
  previousSchool: string;
  applicationStatus: 'pending' | 'approved' | 'rejected';
  documents: {
    oLevelResults: string;
    birthCertificate: string;
    nationalId: string;
  };
  submittedAt: string;
}

export interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  timestamp: string;
}

export interface AdminState {
  students: Student[];
  selectedStudent: Student | null;
  searchQuery: string;
  statusFilter: string;
  notifications: Notification[];
  isLoading: boolean;
  error: string | null;
}