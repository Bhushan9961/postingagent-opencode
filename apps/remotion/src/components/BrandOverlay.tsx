import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion"
import { interpolate } from "remotion"

export const BrandOverlay: React.FC = () => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()
  const opacity = interpolate(frame, [fps * 0.5, fps], [0, 1], {
    extrapolateStart: "clamp",
    extrapolateEnd: "clamp",
  })

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "flex-end",
        padding: 20,
        opacity,
      }}
    >
      <div
        style={{
          fontSize: 14,
          color: "#94a3b8",
          fontFamily: "system-ui",
        }}
      >
        AI Marketing OS
      </div>
    </AbsoluteFill>
  )
}
