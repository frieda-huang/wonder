import { Separator } from "@/components/ui/separator";
import { ExternalLink, Map, Shield, TrendingUp } from "lucide-react";
import { Job } from "./data";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface JobDisplayProps {
  job: Job | null;
}

interface LinkProps {
  link: string;
  label: string;
  type: "default" | "outline";
}

export function Link({ link, label, type }: LinkProps) {
  return (
    <Button className="rounded-2xl" variant={type}>
      <a
        href={link}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center"
      >
        <ExternalLink className="mr-2 h-5 w-5" /> {label}
      </a>
    </Button>
  );
}

export function JobDisplay({ job }: JobDisplayProps) {
  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded-lg shadow-lg space-y-6">
      {/* Job Header */}
      <div className="text-2xl font-semibold text-gray-800">
        {job?.role_name}
      </div>
      <div className="text-lg text-gray-600">{job?.company_name}</div>

      {/* Description */}
      <p className="text-sm text-gray-500">{job?.description}</p>

      {/* Links */}
      <div className="flex gap-4 mt-4">
        <Link link={job!.link_to_website} label="Website" type="default" />
        <Link link={job!.link_to_job} label="Go to job" type="outline" />
      </div>

      <Separator />

      {/* Categories */}
      <div>
        <h4 className="text-sm font-semibold text-gray-700 mb-2">Categories</h4>
        <div className="flex flex-wrap gap-2">
          {job?.categories.map((category, index) => (
            <Badge key={index} variant="secondary" className="text-xs">
              {category}
            </Badge>
          ))}
        </div>
      </div>

      {/* Experience Level */}
      <div>
        <div className="flex items-center space-x-2 text-gray-700">
          <TrendingUp className="h-5 w-5 text-green-500" />
          <h4 className="text-sm font-semibold">Experience Level</h4>
        </div>
        <Badge variant="outline" className="text-xs px-2 py-1 mt-2">
          {job?.experience_level}
        </Badge>
      </div>

      {/* Skills */}
      <div>
        <div className="flex items-center space-x-2 text-gray-700 mb-2">
          <Shield className="h-5 w-5 text-gray-500" />
          <h4 className="text-sm font-semibold">Required Skills</h4>
        </div>
        <div className="flex flex-wrap gap-2">
          {job?.required_skills.map((skill, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {skill}
            </Badge>
          ))}
        </div>
      </div>

      {/* Location */}
      <div className="flex items-center text-sm text-gray-600 space-x-2">
        <Map className="h-5 w-5 text-gray-500" />
        <span className="font-semibold">{job?.location}</span>
      </div>
    </div>
  );
}
