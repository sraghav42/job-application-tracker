import JobApplicationTable from "../components/JobApplicationTable";

function Dashboard() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Job Application Tracker</h1>
      <JobApplicationTable />
    </div>
  );
}

export default Dashboard;
