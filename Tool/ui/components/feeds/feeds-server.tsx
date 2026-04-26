import { fetchScanNotifications } from "@/actions/feeds";

import { FeedsClient } from "./feeds-client";

interface FeedsServerProps {
  limit?: number;
}

export async function FeedsServer({ limit = 15 }: FeedsServerProps) {
  const data = await fetchScanNotifications(limit);
  return <FeedsClient data={data} />;
}
