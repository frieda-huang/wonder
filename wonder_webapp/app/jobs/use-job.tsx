import { atom, useAtom } from "jotai";
import { useEffect } from "react";

import { Job } from "./data";

type Config = {
  selected: Job["id"] | null;
};

const configAtom = atom<Config>({
  selected: null,
});

export function useJob(jobs: Job[]) {
  const [config, setConfig] = useAtom(configAtom);

  useEffect(() => {
    if (!config.selected && jobs.length > 0) {
      setConfig({ selected: jobs[0].id });
    }
  }, [jobs, config.selected, setConfig]);

  return {
    selectedJobId: config.selected,
    setSelectedJobId: (id: Job["id"]) => setConfig({ selected: id }),
  };
}
