import { AbsoluteFill, Sequence, useVideoConfig } from "remotion"
import { BrandOverlay } from "../components/BrandOverlay"
import { CaptionOverlay } from "../components/CaptionOverlay"

interface MarketingVideoProps {
  scenes?: Array<{
    caption: string
    imageUrl?: string
    duration?: number
  }>
  brandColor?: string
}

export const MarketingVideo: React.FC<MarketingVideoProps> = ({
  scenes = [],
  brandColor = "#3b82f6",
}) => {
  const { fps } = useVideoConfig()
  const defaultDuration = 3 * fps

  if (scenes.length === 0) {
    scenes = [
      { caption: "Your AI Marketing Operating System", duration: defaultDuration },
      { caption: "Research. Create. Publish. Learn.", duration: defaultDuration },
    ]
  }

  let currentFrame = 0

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f172a" }}>
      {scenes.map((scene, index) => {
        const startFrame = currentFrame
        currentFrame += scene.duration ?? defaultDuration
        return (
          <Sequence key={index} from={startFrame} durationInFrames={scene.duration ?? defaultDuration}>
            <CaptionOverlay text={scene.caption} color={brandColor} />
            <BrandOverlay />
          </Sequence>
        )
      })}
    </AbsoluteFill>
  )
}
