import { useState, useEffect } from "react";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

function JobApplicationTable() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [sortOrder, setSortOrder] = useState("desc");
  const [selectedJob, setSelectedJob] = useState(null);

  // Fetch job applications from backend
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/jobs");
        if (response.ok) {
          const data = await response.json();
          setJobs(data);
        } else {
          console.error("Failed to fetch jobs");
        }
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };
    fetchJobs();
  }, []);

  // Filter & Sort jobs
  const filteredJobs = jobs
    .filter((job) =>
      job.title.toLowerCase().includes(search.toLowerCase()) || 
      job.company.toLowerCase().includes(search.toLowerCase())
    )
    .filter((job) => (statusFilter && statusFilter !== "all" ? job.status === statusFilter : true))
    .sort((a, b) => (sortOrder === "asc" ? a.date.localeCompare(b.date) : b.date.localeCompare(a.date)));

  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <Input 
          placeholder="Search jobs..." 
          value={search} 
          onChange={(e) => setSearch(e.target.value)} 
          className="w-full max-w-md"
        />

        <Select onValueChange={setStatusFilter} value={statusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Filter by Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem value="Applied">Applied</SelectItem>
            <SelectItem value="Interview">Interview</SelectItem>
            <SelectItem value="Rejected">Rejected</SelectItem>
          </SelectContent>
        </Select>

        <Button onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}>
          Sort by Date {sortOrder === "asc" ? "⬆️" : "⬇️"}
        </Button>
      </div>
      
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Job Title</TableHead>
            <TableHead>Company</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Date Applied</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredJobs.length > 0 ? (
            filteredJobs.map((job) => (
              <TableRow key={job.id}>
                <TableCell>{job.title}</TableCell>
                <TableCell>{job.company}</TableCell>
                <TableCell>{job.status}</TableCell>
                <TableCell>{job.date}</TableCell>
                <TableCell>
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button onClick={() => setSelectedJob(job)}>View Details</Button>
                    </DialogTrigger>
                    <DialogContent>
                      {selectedJob && (
                        <div>
                          <h2 className="text-xl font-bold">{selectedJob.title}</h2>
                          <p className="text-gray-600">{selectedJob.company}</p>
                          <p className="mt-2">{selectedJob.description}</p>
                        </div>
                      )}
                    </DialogContent>
                  </Dialog>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan="5" className="text-center py-4">
                No job applications found.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}

export default JobApplicationTable;
