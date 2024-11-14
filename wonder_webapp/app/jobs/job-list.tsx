import { ComponentProps } from "react";

import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";

import { MapPin } from "lucide-react";
import { Job } from "./data";
import { useJob } from "./use-job";

interface JobListProps {
  items: Job[];
}

export function JobList({ items }: JobListProps) {
  const [job, setJob] = useJob();

  return (
    <ScrollArea className="h-screen">
      <div className="flex flex-col gap-2 p-4 pt-0">
        {items.map((item) => (
          <button
            key={item.id}
            className={cn(
              "flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-xl transition-all hover:bg-accent",
              job.selected === item.id && "bg-muted",
            )}
            onClick={() =>
              setJob({
                ...job,
                selected: item.id,
              })
            }
          >
            <div className="flex w-full flex-col gap-1">
              <div className="flex items-center">
                <div className="flex items-center gap-2">
                  <div className="font-semibold">{item.role_name}</div>
                </div>
              </div>
              <div className="text-sm font-normal">{item.company_name}</div>
            </div>
            <div className="line-clamp-2 text-xs text-muted-foreground">
              {item.description.substring(0, 300)}
            </div>
            {item.required_skills.length ? (
              <div className="flex items-center gap-2">
                {item.required_skills.map((label) => (
                  <Badge key={label} variant={getBadgeVariantFromLabel(label)}>
                    {label}
                  </Badge>
                ))}
              </div>
            ) : null}

            <div className="flex w-full mt-5 items-center text-sm text-orange-500">
              <MapPin className="h-4 w-4 mr-1" />
              {item.location}
            </div>
          </button>
        ))}
      </div>
    </ScrollArea>
  );
}

function getBadgeVariantFromLabel(
  label: string,
): ComponentProps<typeof Badge>["variant"] {
  if (["python"].includes(label.toLowerCase())) {
    return "default";
  }

  if (["machine learning"].includes(label.toLowerCase())) {
    return "lime";
  }

  if (["typescript"].includes(label.toLowerCase())) {
    return "secondary";
  }

  return "outline";
}
