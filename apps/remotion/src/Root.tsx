import { Composition } from "remotion"
import { MarketingVideo } from "./compositions/MarketingVideo"

export const Root: React.FC = () => {
  return (
    <Composition
      id="MarketingVideo"
      component={MarketingVideo}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
    />
  )
}
