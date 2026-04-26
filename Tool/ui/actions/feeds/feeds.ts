"use server";

import { apiBaseUrl, getAuthHeaders } from "@/lib";

import type { ScanNotification, ScanNotificationsData } from "./types";

// Fetch recent completed / failed / cancelled scans as notifications
export async function fetchScanNotifications(
  limit = 15,
): Promise<ScanNotificationsData> {
  try {
    const headers = await getAuthHeaders({ contentType: false });

    const url = new URL(`${apiBaseUrl}/scans`);
    url.searchParams.append("page[size]", String(limit));
    url.searchParams.append("sort", "-completed_at");
    url.searchParams.append("filter[state__in]", "completed,failed,cancelled");
    url.searchParams.append("include", "provider");

    const response = await fetch(url.toString(), {
      headers,
      cache: "no-store",
    });

    if (!response.ok) {
      return { items: [], totalCount: 0 };
    }

    const json = await response.json();
    const scans = json?.data ?? [];
    const included = json?.included ?? [];

    // Build a provider lookup map
    const providerMap = new Map<
      string,
      { type?: string; alias?: string; uid?: string }
    >();
    for (const inc of included) {
      if (inc.type === "providers") {
        providerMap.set(inc.id, {
          type: inc.attributes?.provider,
          alias: inc.attributes?.alias,
          uid: inc.attributes?.uid,
        });
      }
    }

    const items: ScanNotification[] = scans.map(
      (scan: {
        id: string;
        attributes: {
          name?: string;
          state: string;
          progress: number;
          duration: number;
          started_at: string | null;
          completed_at: string | null;
          trigger: "manual" | "scheduled";
        };
        relationships?: {
          provider?: { data?: { id?: string } };
        };
      }) => {
        const providerId = scan.relationships?.provider?.data?.id;
        const provider = providerId ? providerMap.get(providerId) : undefined;

        return {
          id: scan.id,
          name: scan.attributes.name,
          state: scan.attributes.state,
          progress: scan.attributes.progress,
          duration: scan.attributes.duration,
          startedAt: scan.attributes.started_at,
          completedAt: scan.attributes.completed_at,
          trigger: scan.attributes.trigger,
          providerType: provider?.type,
          providerAlias: provider?.alias,
          providerUid: provider?.uid,
        };
      },
    );

    return { items, totalCount: items.length };
  } catch (error) {
    console.error("Error fetching scan notifications:", error);
    return { items: [], totalCount: 0 };
  }
}
