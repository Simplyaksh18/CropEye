// src/components/animations/ScrollFloat.tsx
// Scroll-triggered floating animation

import React, { useEffect, useMemo, useRef } from "react";
import type { ReactNode, RefObject } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

interface ScrollFloatProps {
  children: ReactNode;
  scrollContainerRef?: RefObject<HTMLElement>;
  containerClassName?: string;
  textClassName?: string;
  animationDuration?: number;
  ease?: string;
  scrollStart?: string;
  scrollEnd?: string;
  stagger?: number;
}

const ScrollFloat: React.FC<ScrollFloatProps> = ({
  children,
  scrollContainerRef,
  containerClassName = "",
  textClassName = "",
  animationDuration = 1,
  ease = "back.inOut(2)",
  scrollStart = "center bottom+=50%",
  scrollEnd = "bottom bottom-=40%",
  stagger = 0.03,
}) => {
  const containerRef = useRef<HTMLHeadingElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  const splitText = useMemo(() => {
    const text = typeof children === "string" ? children : "";
    return text.split("").map((char, index) => (
      <span className="inline-block word" key={index}>
        {char === " " ? "\u00A0" : char}
      </span>
    ));
  }, [children]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const scroller: HTMLElement | Window =
      scrollContainerRef && scrollContainerRef.current
        ? (scrollContainerRef.current as HTMLElement)
        : window;

    const charElements = el.querySelectorAll<HTMLElement>(".inline-block");
    if (!charElements || charElements.length === 0) return;

    // cleanup previous timeline/trigger if present
    if (tlRef.current) {
      try {
        tlRef.current.kill();
      } catch {
        /* ignore */
      }
      tlRef.current = null;
    }

    const tl = gsap.timeline();

    tl.fromTo(
      charElements,
      {
        willChange: "opacity, transform",
        opacity: 0,
        yPercent: 120,
        scaleY: 2.3,
        scaleX: 0.7,
        transformOrigin: "50% 0%",
      },
      {
        duration: animationDuration,
        ease: ease,
        opacity: 1,
        yPercent: 0,
        scaleY: 1,
        scaleX: 1,
        stagger: stagger,
        immediateRender: false,
      }
    );

    const st = ScrollTrigger.create({
      trigger: el,
      scroller,
      start: scrollStart,
      end: scrollEnd,
      scrub: true,
      onUpdate: (self: { progress: number }) => {
        tl.progress(self.progress);
      },
    });

    tlRef.current = tl;

    return () => {
      try {
        st.kill();
      } catch {
        /* ignore */
      }
      try {
        tl.kill();
      } catch {
        /* ignore */
      }
    };
  }, [
    scrollContainerRef,
    animationDuration,
    ease,
    scrollStart,
    scrollEnd,
    stagger,
  ]);

  return (
    <h2
      ref={containerRef}
      className={`my-5 overflow-hidden ${containerClassName}`}
    >
      <span
        className={`inline-block text-[clamp(1.6rem,4vw,3rem)] leading-[1.5] ${textClassName}`}
      >
        {splitText}
      </span>
    </h2>
  );
};

export default ScrollFloat;
// also provide named export for compatibility with imports that expect { ScrollFloat }
export { ScrollFloat };
