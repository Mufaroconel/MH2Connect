import React from "react";
import { User, Lock, Bell, Shield, Mail, Smartphone } from "lucide-react";

export default function SettingsPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500 mt-1">
          Manage your account and system preferences
        </p>
      </div>

      <div className="grid gap-6">
        <section className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Profile Settings
          </h2>
          <div className="flex items-center gap-6 mb-6">
            <div className="w-24 h-24 rounded-full bg-emerald-100 flex items-center justify-center">
              <span className="text-2xl font-semibold text-emerald-600">
                JD
              </span>
            </div>
            <div>
              <h3 className="font-medium text-gray-900">John Doe</h3>
              <p className="text-gray-500 text-sm">Administrator</p>
              <button className="mt-2 text-sm text-emerald-600 hover:text-emerald-700">
                Change Profile Picture
              </button>
            </div>
          </div>

          <div className="grid gap-4">
            <SettingsField icon={<User />} label="Full Name" value="John Doe" />
            <SettingsField
              icon={<Mail />}
              label="Email"
              value="john.doe@mufakose2.edu"
            />
            <SettingsField
              icon={<Smartphone />}
              label="Phone"
              value="+263 77 123 4567"
            />
          </div>

          <button className="mt-6 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
            Update Profile
          </button>
        </section>

        <section className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Security Settings
          </h2>
          <div className="space-y-4">
            <SecurityOption
              icon={<Lock />}
              title="Password"
              description="Change your account password"
            />
            <SecurityOption
              icon={<Shield />}
              title="Two-Factor Authentication"
              description="Add an extra layer of security to your account"
            />
            <SecurityOption
              icon={<Bell />}
              title="Notification Preferences"
              description="Manage your notification settings"
            />
          </div>
        </section>
      </div>
    </div>
  );
}

function SettingsField({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center text-gray-500">
        {icon}
      </div>
      <div className="flex-1">
        <label className="block text-sm font-medium text-gray-500">
          {label}
        </label>
        <input
          type="text"
          value={value}
          className="mt-1 block w-full rounded-md border-gray-200 shadow-sm focus:border-emerald-500 focus:ring-emerald-500"
        />
      </div>
    </div>
  );
}

function SecurityOption({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex items-center gap-4 p-4 rounded-lg border border-gray-100 hover:bg-gray-50">
      <div className="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center text-gray-500">
        {icon}
      </div>
      <div className="flex-1">
        <h3 className="font-medium text-gray-900">{title}</h3>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
      <button className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50">
        Manage
      </button>
    </div>
  );
}
