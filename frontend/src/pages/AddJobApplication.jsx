import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

function AddJobApplication() {
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [status, setStatus] = useState("Applied");
  const [date, setDate] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newJob = { title, company, status, date };
  
    try {
      const response = await fetch("http://localhost:5000/api/jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newJob),
      });
  
      if (response.ok) {
        console.log("Job added successfully");
        navigate("/");
      } else {
        console.error("Failed to add job");
      }
    } catch (error) {
      console.error("Error adding job:", error);
    }
  };
  

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Add Job Application</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input placeholder="Job Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <Input placeholder="Company Name" value={company} onChange={(e) => setCompany(e.target.value)} required />
        <Select onValueChange={setStatus} value={status}>
          <SelectTrigger variant="default" className="w-48 bg-white text-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
            <SelectValue>{status}</SelectValue>
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Applied">Applied</SelectItem>
            <SelectItem value="Interview">Interview</SelectItem>
            <SelectItem value="Rejected">Rejected</SelectItem>
          </SelectContent>
        </Select>
        <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        <Button type="submit" className="w-full">Add Job</Button>
        <Button type="button" className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-lg" variant="outline" onClick={() => navigate("/")}>Cancel</Button>
      </form>
    </div>
  );
}

export default AddJobApplication;
