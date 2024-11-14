"use client";

import * as React from "react";

import { cn } from "@/lib/utils";

import { JobList } from "./job-list";

import { type Job } from "./data";
import { JobDisplay } from "./job-display";

import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { useJob } from "./use-job";

interface JobProps {
  jobs: Job[];
  defaultLayout: number[] | undefined;
  defaultCollapsed?: boolean;
  navCollapsedSize: number;
}

export function Job({
  jobs,
  defaultLayout = [20, 32, 48],
  defaultCollapsed = false,
  navCollapsedSize,
}: JobProps) {
  const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed);
  const { selectedJobId } = useJob(jobs);

  return (
    <ResizablePanelGroup
      direction="horizontal"
      onLayout={(sizes: number[]) => {
        document.cookie = `react-resizable-panels:layout:mail=${JSON.stringify(
          sizes,
        )}`;
      }}
      className="h-full max-h-[800px] items-stretch"
    >
      <ResizablePanel
        defaultSize={defaultLayout[0]}
        collapsedSize={navCollapsedSize}
        collapsible={true}
        minSize={15}
        maxSize={20}
        onCollapse={() => {
          setIsCollapsed(true);
          document.cookie = `react-resizable-panels:collapsed=${JSON.stringify(
            true,
          )}`;
        }}
        onResize={() => {
          setIsCollapsed(false);
          document.cookie = `react-resizable-panels:collapsed=${JSON.stringify(
            false,
          )}`;
        }}
        className={cn(
          isCollapsed && "min-w-[50px] transition-all duration-300 ease-in-out",
        )}
      ></ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel defaultSize={defaultLayout[1]} minSize={30}>
        <div className="flex items-center px-4 py-2">
          <h1 className="text-xl font-bold">Jobs</h1>
        </div>
        <JobList items={jobs} />
      </ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel defaultSize={defaultLayout[2]} minSize={30}>
        <JobDisplay
          job={jobs.find((item) => item.id === selectedJobId) || null}
        />
      </ResizablePanel>
    </ResizablePanelGroup>
  );
}
