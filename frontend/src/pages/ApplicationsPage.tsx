import React, { useState } from "react";
import { Student, studentService } from "../services/studentService";
import { format } from "date-fns";
import { ChevronDown, ChevronUp } from "lucide-react";

export default function ApplicationsPage() {
  const [applications, setApplications] = React.useState<Student[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [editMode, setEditMode] = useState<number | null>(null);
  const [editedStudent, setEditedStudent] = useState<Partial<Student> | null>(
    null
  );

  React.useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    try {
      setLoading(true);
      const data = await studentService.getAllStudents();
      setApplications(data);
    } catch (err) {
      setError("Failed to load applications");
      console.error("Error loading applications:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    if (editedStudent) {
      setEditedStudent({ ...editedStudent, [field]: value });
    }
  };

  const handleUpdateStudent = async (student: Student) => {
    if (editedStudent) {
      try {
        await studentService.updateStudentState(
          student.student.whatsapp_number,
          editedStudent.state || student.student.state
        );
        loadApplications();
        setEditMode(null);
        setEditedStudent(null);
      } catch (err) {
        console.error("Error updating student:", err);
      }
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-600">{error}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Applications</h1>
      <p className="text-gray-500 mb-6">
        Review and process new student applications
      </p>

      <div className="space-y-6">
        {applications.map((application) => (
          <div
            key={application.student.id}
            className="bg-white rounded-lg border border-gray-200 p-6"
          >
            {/* Header Section */}
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  {application.student.name}
                </h2>
                <p className="text-sm text-gray-500 mt-1">
                  Applied on {format(new Date(), "MMMM d, yyyy")}
                </p>
              </div>
              <button
                onClick={() =>
                  setExpandedId(
                    expandedId === application.student.id
                      ? null
                      : application.student.id
                  )
                }
                className="text-gray-500 hover:text-gray-700"
              >
                {expandedId === application.student.id ? (
                  <ChevronUp />
                ) : (
                  <ChevronDown />
                )}
              </button>
            </div>

            {/* Default Information Displayed */}
            <div className="grid grid-cols-2 gap-4">
              <InfoField
                label="Email"
                value={application.student.email}
                editable={editMode === application.student.id}
                onChange={(value) => handleInputChange("email", value)}
              />
              <InfoField
                label="WhatsApp"
                value={application.student.whatsapp_number}
                editable={editMode === application.student.id}
                onChange={(value) =>
                  handleInputChange("whatsapp_number", value)
                }
              />
              <InfoField
                label="Gender"
                value={application.student.gender}
                editable={editMode === application.student.id}
                onChange={(value) => handleInputChange("gender", value)}
              />
              <InfoField
                label="Date of Birth"
                value={application.student.dob}
                editable={editMode === application.student.id}
                onChange={(value) => handleInputChange("dob", value)}
              />
              <InfoField
                label="Address"
                value={application.student.address}
                editable={editMode === application.student.id}
                onChange={(value) => handleInputChange("address", value)}
              />
              <InfoField
                label="Application Status"
                value={application.student.state}
                editable={editMode === application.student.id}
                onChange={(value) => handleInputChange("state", value)}
              />
            </div>

            {/* Image Section for Academic History */}
            <div className="mt-4">
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Uploaded Documents
              </h3>
              <div className="flex space-x-4">
                {application.academic_history.path1 && (
                  <img
                    src={application.academic_history.path1}
                    alt="Document 1"
                    className="w-48 h-48 object-cover rounded border"
                  />
                )}
                {application.academic_history.path2 && (
                  <img
                    src={application.academic_history.path2}
                    alt="Document 2"
                    className="w-48 h-48 object-cover rounded border"
                  />
                )}
                {application.academic_history.path3 && (
                  <img
                    src={application.academic_history.path3}
                    alt="Document 3"
                    className="w-48 h-48 object-cover rounded border"
                  />
                )}
              </div>
            </div>

            {/* Edit and Save Buttons */}
            <div className="mt-4">
              {editMode === application.student.id ? (
                <button
                  onClick={() => handleUpdateStudent(application)}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Save
                </button>
              ) : (
                <button
                  onClick={() => {
                    setEditMode(application.student.id);
                    setEditedStudent({ ...application });
                  }}
                  className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                >
                  Edit
                </button>
              )}
            </div>

            {/* Expanded Details */}
            {expandedId === application.student.id && (
              <div className="mt-4 space-y-6">
                {/* Academic History */}
                <div className="border-t pt-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    Academic History
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    {Array.from({ length: 14 }, (_, i) => i + 1).map((num) => {
                      const subject =
                        application.academic_history[`subject${num}`];
                      const symbol =
                        application.academic_history[`symbol${num}`];
                      if (subject && symbol) {
                        return (
                          <div
                            key={num}
                            className="flex justify-between items-center"
                          >
                            <span className="text-gray-600">{subject}</span>
                            <span className="font-medium">{symbol}</span>
                          </div>
                        );
                      }
                      return null;
                    })}
                  </div>
                </div>

                {/* Subject Combinations */}
                <div className="border-t pt-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    Subject Combinations
                  </h3>
                  <div className="space-y-4">
                    <CombinationOption
                      label="First Choice"
                      subjects={[
                        application.subject_combination.subject1,
                        application.subject_combination.subject2,
                        application.subject_combination.subject3,
                      ]}
                    />
                    <CombinationOption
                      label="Second Choice"
                      subjects={[
                        application.subject_combination.subject1_option2,
                        application.subject_combination.subject2_option2,
                        application.subject_combination.subject3_option2,
                      ]}
                    />
                    <CombinationOption
                      label="Third Choice"
                      subjects={[
                        application.subject_combination.subject1_option3,
                        application.subject_combination.subject2_option3,
                        application.subject_combination.subject3_option3,
                      ]}
                    />
                  </div>
                </div>

                {/* Required Documents */}
                <div className="border-t pt-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    Required Documents
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <DocumentStatus
                      label="Birth Certificate"
                      path={application.academic_history.path1}
                    />
                    <DocumentStatus
                      label="O-Level Results"
                      path={application.academic_history.path2}
                    />
                    <DocumentStatus
                      label="Passport Photo"
                      path={application.academic_history.path3}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function InfoField({
  label,
  value,
  editable,
  onChange,
}: {
  label: string;
  value: string | null | undefined;
  editable: boolean;
  onChange: (value: string) => void;
}) {
  return (
    <div>
      <span className="text-sm text-gray-500">{label}</span>
      {editable ? (
        <input
          type="text"
          defaultValue={value || ""}
          onChange={(e) => onChange(e.target.value)}
          className="mt-1 block w-full border border-gray-300 rounded p-1"
        />
      ) : (
        <p className="text-sm font-medium text-gray-900">
          {value || "Not provided"}
        </p>
      )}
    </div>
  );
}

function CombinationOption({
  label,
  subjects,
}: {
  label: string;
  subjects: (string | null)[];
}) {
  const validSubjects = subjects.filter(Boolean);
  if (validSubjects.length === 0) return null;

  return (
    <div className="p-3 rounded-lg bg-gray-50">
      <span className="text-sm font-medium text-gray-700">{label}</span>
      <p className="mt-1 text-sm text-gray-600">{validSubjects.join(", ")}</p>
    </div>
  );
}

function DocumentStatus({
  label,
  path,
}: {
  label: string;
  path: string | null;
}) {
  const isUploaded = !!path;

  return (
    <div className="flex items-center gap-2">
      <div
        className={`w-5 h-5 rounded-full flex items-center justify-center ${
          isUploaded ? "bg-green-100" : "bg-gray-100"
        }`}
      >
        <div
          className={`w-2 h-2 rounded-full ${
            isUploaded ? "bg-green-600" : "bg-gray-400"
          }`}
        />
      </div>
      <span className="text-sm text-gray-600">{label}</span>
    </div>
  );
}
