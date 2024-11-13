"use client";

import { z } from "zod";
import { useForm } from "react-hook-form";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";

type AccountFormValues = z.infer<typeof preferencesFormSchema>;

const preferencesFormSchema = z.object({
  location: z.string({
    required_error: "Please select a role.",
  }),
  resume: z.instanceof(File).refine(
    (file) => file.size < 7 * 1024 * 1024, // 7MB in bytes
    {
      message: "Your resume must be less than 7MB",
    },
  ),
  roles: z.array(z.string()).min(0),
  aspirations: z.string({
    required_error: "Tell us about your aspirations.",
  }),
});

const locations = [
  { label: "San Francisco", value: "San Francisco" },
  { label: "Silicon Valley", value: "Silicon Valley" },
  { label: "New York City", value: "New York City" },
  { label: "Austin", value: "Austin" },
] as const;

const roles = [
  {
    id: "AI & Machine Learning",
    label: "AI & Machine Learning",
  },
  {
    id: "Full Stack",
    label: "Full Stack",
  },
  {
    id: "Backend",
    label: "Backend",
  },
  {
    id: "Frontend",
    label: "Frontend",
  },
  {
    id: "Data Science",
    label: "Data Science",
  },
  {
    id: "System & Infrastructure",
    label: "System & Infrastructure",
  },
] as const;

// This can come from your database or API.
const defaultValues: Partial<AccountFormValues> = {
  location: "",
  resume: undefined,
  roles: [],
  aspirations: "",
};

export default function Page() {
  const form = useForm<AccountFormValues>({
    resolver: zodResolver(preferencesFormSchema),
    defaultValues,
  });

  function onSubmit(data: AccountFormValues) {
    console.log(data);
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

  return (
    <div className="flex items-center justify-center">
      <div className="w-1/3">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            {/* Location */}
            <FormField
              control={form.control}
              name="location"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel className="text-base">Location</FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className={cn(
                            "w-full justify-between",
                            !field.value && "text-muted-foreground",
                          )}
                        >
                          {field.value
                            ? locations.find(
                                (location) => location.value === field.value,
                              )?.label
                            : "Select location"}
                          <ChevronsUpDown className="opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
                      <Command>
                        <CommandInput placeholder="Search location..." />
                        <CommandList>
                          <CommandEmpty>No role found.</CommandEmpty>
                          <CommandGroup>
                            {locations.map((location) => (
                              <CommandItem
                                value={location.label}
                                key={location.value}
                                onSelect={() => {
                                  form.setValue("location", location.value);
                                }}
                              >
                                <Check
                                  className={cn(
                                    "mr-2",
                                    location.value === field.value
                                      ? "opacity-100"
                                      : "opacity-0",
                                  )}
                                />
                                {location.label}
                              </CommandItem>
                            ))}
                          </CommandGroup>
                        </CommandList>
                      </Command>
                    </PopoverContent>
                  </Popover>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Resume */}
            <FormField
              control={form.control}
              name="resume"
              render={({ field: { value, onChange, ...fieldProps } }) => (
                <FormItem className="grid w-full items-center gap-1.5">
                  <FormLabel className="text-base">Resume</FormLabel>
                  <FormControl>
                    <Input
                      {...fieldProps}
                      type="file"
                      accept="application/pdf"
                      onChange={(event) =>
                        onChange(event.target.files && event.target.files[0])
                      }
                    />
                  </FormControl>
                </FormItem>
              )}
            />

            {/* Role Type */}
            <FormField
              control={form.control}
              name="roles"
              render={() => (
                <FormItem>
                  <div className="mb-4">
                    <FormLabel className="text-base">Role Type</FormLabel>
                  </div>
                  {roles.map((role) => (
                    <FormField
                      key={role.id}
                      control={form.control}
                      name="roles"
                      render={({ field }) => {
                        return (
                          <FormItem
                            key={role.id}
                            className="flex flex-row items-start space-x-3 space-y-0"
                          >
                            <FormControl>
                              <Checkbox
                                checked={field.value?.includes(role.id)}
                                onCheckedChange={(checked) => {
                                  return checked
                                    ? field.onChange([...field.value, role.id])
                                    : field.onChange(
                                        field.value?.filter(
                                          (value) => value !== role.id,
                                        ),
                                      );
                                }}
                              />
                            </FormControl>
                            <FormLabel className="font-normal">
                              {role.label}
                            </FormLabel>
                          </FormItem>
                        );
                      }}
                    />
                  ))}
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* What are you looking for in your next position? */}
            <FormField
              control={form.control}
              name="aspirations"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="text-base">
                    What are you looking for in your next position?
                  </FormLabel>
                  <FormControl>
                    <Textarea className="resize-none h-40" {...field} />
                  </FormControl>
                </FormItem>
              )}
            />
            <Button className="w-full" type="submit">
              Save
            </Button>
          </form>
        </Form>
      </div>
    </div>
  );
}
