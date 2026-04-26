import {
  CloudCog,
  Cog,
  GitBranch,
  Mail,
  MessageCircleQuestion,
  Puzzle,
  Settings,
  ShieldCheck,
  SquareChartGantt,
  Tag,
  Timer,
  User,
  UserCog,
  Users,
  VolumeX,
  Warehouse,
} from "lucide-react";

import {
  APIdocIcon,
  LighthouseIcon,
  SupportIcon,
} from "@/components/icons/Icons";
import { GroupProps } from "@/types";

interface MenuListOptions {
  pathname: string;
}

export const getMenuList = ({ pathname }: MenuListOptions): GroupProps[] => {
  return [
    {
      groupLabel: "",
      menus: [
        {
          href: "/",
          label: "Overview",
          icon: SquareChartGantt,
          active: pathname === "/",
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "/compliance",
          label: "Compliance",
          icon: ShieldCheck,
          active: pathname === "/compliance",
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "/lighthouse",
          label: "Lighthouse AI",
          icon: LighthouseIcon,
          active: pathname === "/lighthouse",
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "/attack-paths",
          label: "Attack Paths",
          icon: GitBranch,
          active: pathname.startsWith("/attack-paths"),
          highlight: true,
        },
      ],
    },

    {
      groupLabel: "",
      menus: [
        {
          href: "/findings?filter[muted]=false&filter[status__in]=FAIL",
          label: "Findings",
          icon: Tag,
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "/resources",
          label: "Resources",
          icon: Warehouse,
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "",
          label: "Configuration",
          icon: Settings,
          submenus: [
            { href: "/providers", label: "Cloud Providers", icon: CloudCog },
            {
              href: "/mutelist",
              label: "Mutelist",
              icon: VolumeX,
              active: pathname === "/mutelist",
            },
            { href: "/scans", label: "Scan Jobs", icon: Timer },
            { href: "/integrations", label: "Integrations", icon: Puzzle },
            { href: "/roles", label: "Roles", icon: UserCog },
            { href: "/lighthouse/config", label: "Lighthouse AI", icon: Cog },
          ],
          defaultOpen: true,
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "",
          label: "Organization",
          icon: Users,
          submenus: [
            { href: "/users", label: "Users", icon: User },
            { href: "/invitations", label: "Invitations", icon: Mail },
          ],
          defaultOpen: false,
        },
      ],
    },
    {
      groupLabel: "",
      menus: [
        {
          href: "",
          label: "Support & Help",
          icon: SupportIcon,
          submenus: [
            {
              href: `${process.env.NEXT_PUBLIC_API_DOCS_URL ?? "/api/v1/docs"}`,
              target: "_blank",
              label: "API reference",
              icon: APIdocIcon,
            },
            {
              href: "mailto:devops@azintelecom.az",
              target: "_blank",
              label: "Contact Support",
              icon: MessageCircleQuestion,
            },
          ],
          defaultOpen: false,
        },
      ],
    },
  ];
};
