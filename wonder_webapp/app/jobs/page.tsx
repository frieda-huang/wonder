import { cookies } from "next/headers";
import { Job } from "./job";

async function fetchJobs() {
  const res = await fetch("http://localhost:8000/get-jobs", {
    cache: "no-store",
  });

  if (!res.ok) {
    console.error("Failed to fetch jobs");
    return [];
  }

  const jobs = await res.json();
  return Array.isArray(jobs) ? jobs : [];
}

export default async function JobPage() {
  const layout = cookies().get("react-resizable-panels:layout:mail");
  const collapsed = cookies().get("react-resizable-panels:collapsed");
  const jobs = await fetchJobs();

  console.log("jobs > ", jobs);

  const defaultLayout = layout ? JSON.parse(layout.value) : undefined;
  const defaultCollapsed = collapsed ? JSON.parse(collapsed.value) : undefined;

  return (
    <>
      <div className="hidden flex-col md:flex">
        {jobs.length > 0 ? (
          <Job
            jobs={jobs}
            defaultLayout={defaultLayout}
            defaultCollapsed={defaultCollapsed}
            navCollapsedSize={4}
          />
        ) : (
          <div>No jobs found. Please submit your preferences first.</div>
        )}
      </div>
    </>
  );
}
