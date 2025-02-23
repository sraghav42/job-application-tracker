import { useState } from "react";
import { Home, Briefcase, Settings } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import JobApplicationTable from "@/components/JobApplicationTable";


const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("applications");

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg p-5 flex flex-col">
        <h1 className="text-2xl font-bold mb-6">Job Tracker</h1>
        <ul>
          <li
            className={`p-3 flex items-center cursor-pointer rounded-xl mb-2 ${
              activeTab === "applications" ? "bg-blue-500 text-white" : "hover:bg-gray-200"
            }`}
            onClick={() => setActiveTab("applications")}
          >
            <Briefcase className="mr-3" /> Applications
          </li>
          <li
            className={`p-3 flex items-center cursor-pointer rounded-xl mb-2 ${
              activeTab === "dashboard" ? "bg-blue-500 text-white" : "hover:bg-gray-200"
            }`}
            onClick={() => setActiveTab("dashboard")}
          >
            <Home className="mr-3" /> Dashboard
          </li>
          <li
            className={`p-3 flex items-center cursor-pointer rounded-xl ${
              activeTab === "settings" ? "bg-blue-500 text-white" : "hover:bg-gray-200"
            }`}
            onClick={() => setActiveTab("settings")}
          >
            <Settings className="mr-3" /> Settings
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6">
        {activeTab === "applications" && (
          <Card>
            <CardContent>
              <h2 className="text-xl font-semibold">Job Applications</h2>
              <p className="text-gray-600">List of job applications will be displayed here.</p>
            </CardContent>
          </Card>
        )}
        {activeTab === "dashboard" && (
          <Card>
            <CardContent>
              <h2 className="text-xl font-semibold">Dashboard Overview</h2>
              <p className="text-gray-600">Summary of job applications and statistics.</p>
              <JobApplicationTable jobApplications={[]} />
            </CardContent>
          </Card>
        )}
        {activeTab === "settings" && (
          <Card>
            <CardContent>
              <h2 className="text-xl font-semibold">Settings</h2>
              <p className="text-gray-600">User settings and preferences.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Dashboard;