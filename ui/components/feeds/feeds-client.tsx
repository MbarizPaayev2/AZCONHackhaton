"use client";

import {
  BellRing,
  CheckCircle2,
  Clock,
  Shield,
  XCircle,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import type { ScanNotification, ScanNotificationsData } from "@/actions/feeds";
import {
  Badge,
  Button,
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  Separator,
} from "@/components/shadcn";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/shadcn/tooltip";
import { formatDuration, formatRelativeTime } from "@/lib/date-utils";
import { hasNewFeeds, markFeedsAsSeen } from "@/lib/feeds-storage";
import { cn } from "@/lib/utils";

interface FeedsClientProps {
  data: ScanNotificationsData;
}

export function FeedsClient({ data }: FeedsClientProps) {
  const { items, totalCount } = data;
  const hasItems = totalCount > 0;

  const [hasUnseen, setHasUnseen] = useState(false);

  useEffect(() => {
    if (hasItems) {
      const ids = items.map((item) => item.id);
      setHasUnseen(hasNewFeeds(ids));
    }
  }, [hasItems, items]);

  const handleOpenChange = (open: boolean) => {
    if (open && hasItems) {
      const ids = items.map((item) => item.id);
      markFeedsAsSeen(ids);
      setHasUnseen(false);
    }
  };

  return (
    <DropdownMenu onOpenChange={handleOpenChange}>
      <Tooltip>
        <TooltipTrigger asChild>
          <DropdownMenuTrigger asChild>
            <Button
              variant="outline"
              className="border-border-input-primary-fill relative h-8 w-8 rounded-full bg-transparent p-2"
              aria-label={
                hasUnseen
                  ? "New scan notifications - Click to view"
                  : "Scan notifications"
              }
            >
              <BellRing
                size={18}
                className={cn(
                  hasItems &&
                    hasUnseen &&
                    "text-button-primary animate-pulse",
                )}
              />
              {hasItems && hasUnseen && (
                <span className="absolute top-0 right-0 flex h-2 w-2">
                  <span className="bg-button-primary absolute inline-flex h-full w-full animate-ping rounded-full opacity-75"></span>
                  <span className="bg-button-primary relative inline-flex h-2 w-2 rounded-full"></span>
                </span>
              )}
            </Button>
          </DropdownMenuTrigger>
        </TooltipTrigger>
        <TooltipContent>
          {hasUnseen ? "New scan notifications" : "Scan Notifications"}
        </TooltipContent>
      </Tooltip>

      <DropdownMenuContent
        align="end"
        className="w-96 gap-2 overflow-x-hidden border-slate-200 bg-white px-[18px] pt-3 pb-4 dark:border-zinc-900 dark:bg-stone-950"
      >
        <div className="pb-2">
          <h3 className="text-base font-semibold text-slate-900 dark:text-white">
            Scan Notifications
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Recent scan completions and results
          </p>
        </div>

        <Separator />

        <div className="minimal-scrollbar max-h-[500px] overflow-x-hidden overflow-y-auto">
          {items.length === 0 && (
            <div className="px-3 py-8 text-center">
              <Shield className="mx-auto mb-2 h-8 w-8 text-slate-400" />
              <p className="text-sm font-medium text-slate-600 dark:text-slate-300">
                No completed scans yet
              </p>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                Notifications will appear here when scans finish
              </p>
            </div>
          )}

          {hasItems && (
            <div className="relative py-2">
              {items.map((item, index) => (
                <ScanNotificationItem
                  key={item.id}
                  item={item}
                  isLast={index === items.length - 1}
                />
              ))}
            </div>
          )}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

interface ScanNotificationItemProps {
  item: ScanNotification;
  isLast: boolean;
}

const stateConfig = {
  completed: {
    icon: CheckCircle2,
    color: "text-emerald-500",
    dotColor: "border-emerald-500 bg-emerald-500",
    label: "Completed",
    badgeClass:
      "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-800 dark:bg-emerald-950 dark:text-emerald-400",
  },
  failed: {
    icon: XCircle,
    color: "text-red-500",
    dotColor: "border-red-500 bg-red-500",
    label: "Failed",
    badgeClass:
      "border-red-200 bg-red-50 text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-400",
  },
  cancelled: {
    icon: XCircle,
    color: "text-amber-500",
    dotColor: "border-amber-500 bg-amber-500",
    label: "Cancelled",
    badgeClass:
      "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-400",
  },
} as const;

function ScanNotificationItem({ item, isLast }: ScanNotificationItemProps) {
  const config =
    stateConfig[item.state as keyof typeof stateConfig] ?? stateConfig.completed;
  const relativeTime = formatRelativeTime(item.completedAt);
  const durationStr = item.duration > 0 ? formatDuration(item.duration) : null;

  const title =
    item.name ||
    (item.providerAlias
      ? `${item.providerAlias} scan`
      : item.providerType
        ? `${item.providerType.toUpperCase()} scan`
        : "Scan");

  return (
    <div className="group relative flex gap-3 px-3 py-2">
      <div className="relative flex flex-col items-center">
        <div
          className={cn(
            "z-10 h-2 w-2 rounded-full border-2",
            config.dotColor,
          )}
        />
        {!isLast && (
          <div className="h-full w-px bg-slate-200 dark:bg-slate-700" />
        )}
      </div>

      <div className="min-w-0 flex-1 pb-4">
        <Link
          href={`/scans`}
          className="backdrop-blur-0 block space-y-1 rounded-[12px] border border-transparent p-2 transition-all hover:border-slate-300 hover:bg-[#F8FAFC80] hover:backdrop-blur-[46px] dark:hover:border-[rgba(38,38,38,0.70)] dark:hover:bg-[rgba(23,23,23,0.50)]"
        >
          <div className="flex items-start justify-between gap-2">
            <h4 className="group-hover:text-button-primary dark:group-hover:text-button-primary min-w-0 flex-1 text-sm leading-tight font-semibold break-words text-slate-900 dark:text-white">
              {title}
            </h4>
            <Badge
              variant="secondary"
              className={cn("shrink-0 text-[10px] font-semibold", config.badgeClass)}
            >
              {config.label}
            </Badge>
          </div>

          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
            {item.providerType && (
              <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-medium uppercase dark:bg-slate-800">
                {item.providerType}
              </span>
            )}
            {item.providerUid && (
              <span className="truncate text-[11px]">{item.providerUid}</span>
            )}
          </div>

          <div className="flex items-center justify-between pt-1">
            <time className="text-[11px] text-slate-500 dark:text-slate-500">
              {relativeTime}
            </time>

            {durationStr && (
              <div className="flex items-center gap-1 text-[11px] text-slate-400">
                <Clock size={10} />
                <span>{durationStr}</span>
              </div>
            )}
          </div>
        </Link>
      </div>
    </div>
  );
}
