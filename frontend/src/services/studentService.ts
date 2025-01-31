import { StudentSchema } from '../types/api';
import { apiClient } from './apiClient';

export interface Student {
  student: {
    id: number;
    whatsapp_number: string;
    name: string;
    email: string;
    state: string;
    dob: string | null;
    gender: string | null;
    address: string | null;
  };
  academic_history: {
    id: number;
    whatsapp_number: string;
    path1: string | null;
    path2: string | null;
    path3: string | null;
    subject1: string | null;
    symbol1: string | null;
    // ... other subjects and symbols
  };
  subject_combination: {
    id: number;
    whatsapp_number: string;
    subject1: string | null;
    subject2: string | null;
    subject3: string | null;
    subject1_option2: string | null;
    subject2_option2: string | null;
    subject3_option2: string | null;
    subject1_option3: string | null;
    subject2_option3: string | null;
    subject3_option3: string | null;
    subject_combination_state: string | null;
    suggested_subject1: string | null;
    suggested_subject2: string | null;
    suggested_subject3: string | null;
  };
}

export const studentService = {
  getAllStudents: async (): Promise<Student[]> => {
    return await apiClient.get('/api/students');
  },

  getStudent: async (whatsappNumber: string): Promise<Student> => {
    return await apiClient.get(`/api/students/${whatsappNumber}`);
  },

  updateStudentState: async (whatsappNumber: string, state: string): Promise<Student> => {
    return await apiClient.patch(`/api/students/${whatsappNumber}/state`, { state });
  },

  updateSubjectCombinationState: async (whatsappNumber: string, state: string): Promise<Student> => {
    return await apiClient.patch(`/api/students/${whatsappNumber}/subject-combination-state`, { state });
  },

  async updateStudentStatus(id: string, status: Student['applicationStatus']) {
    const response = await apiClient.patch(`/api/students/${id}/status`, { status });
    return StudentSchema.parse(response.data);
  },

  async uploadDocument(studentId: string, documentType: string, file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post(
      `/api/students/${studentId}/documents/${documentType}`,
      formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
    );
    return StudentSchema.parse(response.data);
  }
};