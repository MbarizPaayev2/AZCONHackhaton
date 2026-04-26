export type SiteConfig = typeof siteConfig;

const isCloudEnv = process.env.NEXT_PUBLIC_IS_CLOUD_ENV === "true";

export const siteConfig = {
  name: isCloudEnv ? "AzCSPM" : "AzCSPM",
  description:
    "AzCSPM is a Cloud Security Platform that automates security and compliance across any cloud environment. With hundreds of ready-to-use security checks, remediation guidance, and compliance frameworks, AzCSPM delivers AI-driven, customizable, and easy-to-use assessments, dashboards, reports, and integrations, making cloud security simple, scalable, and cost-effective for organizations of any size.",
};
