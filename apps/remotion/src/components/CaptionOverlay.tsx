import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion"
import { interpolate } from "remotion"

interface CaptionOverlayProps {
  text: string
  color?: string
}

export const CaptionOverlay: React.FC<CaptionOverlayProps> = ({
  text,
  color = "#3b82f6",
}) => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()
  const duration = 3 * fps
  const opacity = interpolate(frame, [0, 15, duration - 15, duration], [0, 1, 1, 0], {
    extrapolateStart: "clamp",
    extrapolateEnd: "clamp",
  })
  const scale = interpolate(frame, [0, 15], [0.9, 1], {
    extrapolateStart: "clamp",
    extrapolateEnd: "clamp",
  })

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity,
        scale: String(scale),
      }}
    >
      <div
        style={{
          fontSize: 48,
          fontWeight: 700,
          color: "#f1f5f9",
          textAlign: "center",
          maxWidth: "80%",
          fontFamily: "system-ui",
          lineHeight: 1.3,
          textShadow: `0 2px 4px rgba(0,0,0,0.5)`,
        }}
      >
        {text.split(" ").map((word, i) => {
          const wordDelay = i * 3
          const wordOpacity = interpolate(frame, [wordDelay, wordDelay + 10], [0, 1], {
            extrapolateStart: "clamp",
            extrapolateEnd: "clamp",
          })
          return (
            <span
              key={i}
              style={{
                opacity: wordOpacity,
                display: "inline-block",
                marginRight: 8,
              }}
            >
              {word}
            </span>
          )
        })}
      </div>
      <div
        style={{
          width: 60,
          height: 4,
          backgroundColor: color,
          borderRadius: 2,
          marginTop: 24,
        }}
      />
    </AbsoluteFill>
  )
}
