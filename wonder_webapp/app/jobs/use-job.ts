import { atom, useAtom } from "jotai";

import { Job, jobs } from "./data";

type Config = {
  selected: Job["id"] | null;
};

const configAtom = atom<Config>({
  selected: jobs[0].id,
});

export function useJob() {
  return useAtom(configAtom);
}
