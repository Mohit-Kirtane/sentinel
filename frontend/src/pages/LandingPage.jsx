import { Architecture } from "../components/landing/Architecture.jsx";
import { Features } from "../components/landing/Features.jsx";
import { Hero } from "../components/landing/Hero.jsx";
import { HowItWorks } from "../components/landing/HowItWorks.jsx";
import { LandingFooter } from "../components/landing/LandingFooter.jsx";
import { LandingHeader } from "../components/landing/LandingHeader.jsx";
import { TechStack } from "../components/landing/TechStack.jsx";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-bg">
      <LandingHeader />
      <Hero />
      <HowItWorks />
      <Features />
      <Architecture />
      <TechStack />
      <LandingFooter />
    </div>
  );
}
