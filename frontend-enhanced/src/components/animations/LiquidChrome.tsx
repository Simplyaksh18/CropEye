// src/components/animations/LiquidChrome.tsx
// Liquid chrome background for login page
// Color Mix: Red 0, Green 0.3, Blue 0.1
// Speed: 0.41, Amplitude: 0.3, Interaction: Enabled

import React, { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

const LiquidChromeShader: React.FC<{ interactive?: boolean }> = ({
  interactive = false,
}) => {
  const meshRef = useRef<THREE.Mesh>(null);

  // detect theme (guard SSR)
  const isDark =
    typeof document !== "undefined" &&
    document.documentElement.classList.contains("dark");

  // Shader material with theme-aware parameters
  const uniforms = useMemo(
    () => ({
      u_time: { value: 0 },
      // theme-aware color mix: greenish in light, cool blue in dark
      u_colorMix: {
        value: isDark
          ? new THREE.Vector3(0.02, 0.28, 0.55) // subtle blue tint for dark
          : new THREE.Vector3(0.0, 0.3, 0.1), // green tint for light
      },
      // slightly different motion feel per theme
      u_speed: { value: isDark ? 0.32 : 0.41 },
      u_amplitude: { value: isDark ? 0.22 : 0.3 },
      // u_interaction will be set from prop below
      u_interaction: { value: interactive ? 1.0 : 0.0 },
    }),
    [interactive, isDark]
  );

  const vertexShader = `
    varying vec2 vUv;
    varying vec3 vPosition;
    uniform float u_time;
    uniform float u_amplitude;
    
    void main() {
      vUv = uv;
      vPosition = position;
      
      vec3 pos = position;
      float wave = sin(pos.x * 2.0 + u_time) * u_amplitude;
      wave += sin(pos.y * 3.0 + u_time * 1.5) * u_amplitude * 0.5;
      pos.z += wave;
      
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `;

  const fragmentShader = `
    uniform float u_time;
    uniform vec3 u_colorMix;
    varying vec2 vUv;
    varying vec3 vPosition;
    
    void main() {
      vec2 uv = vUv;
      
      // Liquid distortion
      vec2 distortion = vec2(
        sin(uv.y * 10.0 + u_time),
        cos(uv.x * 10.0 + u_time)
      ) * 0.1;
      
      uv += distortion;
      
      // Chrome-like gradient
      vec3 color1 = vec3(0.1, 0.1, 0.1);
      vec3 color2 = vec3(0.9, 0.9, 0.9);
      vec3 color3 = u_colorMix;
      
      float pattern = sin(uv.x * 15.0 + u_time) * cos(uv.y * 15.0 + u_time);
      vec3 color = mix(color1, color2, pattern);
      color = mix(color, color3, 0.3);
      
      // Chrome reflections
      float reflection = pow(abs(sin(vPosition.z * 2.0 + u_time)), 2.0);
      color += vec3(reflection * 0.5);
      
      gl_FragColor = vec4(color, 1.0);
    }
  `;

  useFrame(({ clock }) => {
    if (meshRef.current) {
      const material = meshRef.current.material as THREE.ShaderMaterial;
      material.uniforms.u_time.value =
        clock.getElapsedTime() * (uniforms.u_speed?.value ?? 1.0);
      // Keep uniform for interaction in sync in case parent toggles it
      material.uniforms.u_interaction.value = uniforms.u_interaction.value;
    }
  });

  return (
    <mesh ref={meshRef} scale={[2, 2, 1]}>
      <planeGeometry args={[10, 10, 64, 64]} />
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
};

export const LiquidChrome: React.FC<{
  className?: string;
  interactive?: boolean;
}> = ({ className = "", interactive = false }) => {
  // When interactive=true we allow pointer events and enable
  // the shader interaction uniform. Otherwise, the background
  // is strictly decorative and won't block inputs.
  return (
    <div
      className={`fixed inset-0 ${className}`}
      style={{
        zIndex: interactive ? 5 : 0,
        pointerEvents: interactive ? "auto" : "none",
      }}
    >
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <LiquidChromeShader interactive={interactive} />
      </Canvas>
    </div>
  );
};

// Usage in Login Page:
// import { LiquidChrome } from '@/components/animations/LiquidChrome';
//
// export const LoginPage = () => {
//   return (
//     <div className="relative min-h-screen">
//       <LiquidChrome />
//       <div className="relative z-10">
//         {/* Login form content */}
//       </div>
//     </div>
//   );
// };
