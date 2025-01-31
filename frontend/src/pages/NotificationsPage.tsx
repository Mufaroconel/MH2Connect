import React from 'react';
import { Bell, CheckCircle, AlertCircle, Clock, Trash2 } from 'lucide-react';

export default function NotificationsPage() {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
          <p className="text-gray-500 mt-1">View system notifications and alerts</p>
        </div>
        <button className="text-gray-500 hover:text-gray-700 flex items-center gap-2">
          <Trash2 className="w-4 h-4" />
          <span>Clear All</span>
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 divide-y divide-gray-100">
        {notifications.map((notification) => (
          <NotificationItem key={notification.id} {...notification} />
        ))}
      </div>
    </div>
  );
}

function NotificationItem({ 
  type, 
  title, 
  message, 
  time 
}: {
  type: 'success' | 'warning' | 'info';
  title: string;
  message: string;
  time: string;
}) {
  const icons = {
    success: <CheckCircle className="w-5 h-5 text-green-500" />,
    warning: <AlertCircle className="w-5 h-5 text-yellow-500" />,
    info: <Bell className="w-5 h-5 text-blue-500" />
  };

  return (
    <div className="p-4 hover:bg-gray-50">
      <div className="flex gap-4">
        <div className="flex-shrink-0">
          {icons[type]}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900">{title}</p>
          <p className="text-sm text-gray-500">{message}</p>
          <div className="mt-1 flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className="text-xs text-gray-500">{time}</span>
          </div>
        </div>
        <button className="text-gray-400 hover:text-gray-500">
          <Trash2 className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

const notifications = [
  {
    id: 1,
    type: 'success' as const,
    title: 'Application Approved',
    message: 'James Moyo\'s application has been successfully approved.',
    time: '2 minutes ago'
  },
  {
    id: 2,
    type: 'warning' as const,
    title: 'Missing Documents',
    message: 'Sarah Banda\'s application is missing required documents.',
    time: '1 hour ago'
  },
  {
    id: 3,
    type: 'info' as const,
    title: 'New Application',
    message: 'David Mutasa has submitted a new enrollment application.',
    time: '3 hours ago'
  },
  {
    id: 4,
    type: 'warning' as const,
    title: 'Document Verification Required',
    message: 'Please verify the O-Level results for David Mutasa\'s application.',
    time: '5 hours ago'
  },
  {
    id: 5,
    type: 'success' as const,
    title: 'Documents Uploaded',
    message: 'Sarah Banda has uploaded the requested documents.',
    time: '1 day ago'
  }
];