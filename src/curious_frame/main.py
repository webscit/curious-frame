# SPDX-FileCopyrightText: 2025-present Frédéric Collonval <frederic.collonval@webscit.com>
#
# SPDX-License-Identifier: MIT
"""Main module for the Curious Frame project."""
import argparse
import csv
from datetime import datetime
from pathlib import Path

from curious_frame.audio import Audio
from curious_frame.camera import Camera
from curious_frame.language import Language
from curious_frame.vision import Vision


def main() -> None:
    """The main function for the Curious Frame project."""
    parser = argparse.ArgumentParser(prog="python3 -m curious_frame", description="Curious Frame: An interactive tutor for kids.")
    parser.add_argument(
        "--camera-id", type=int, default=0, help="The ID of the camera to use (default: 0)."
    )
    parser.add_argument(
        "--width", type=int, default=1280, help="The width of the camera frame (default: 1280)."
    )
    parser.add_argument(
        "--height", type=int, default=720, help="The height of the camera frame (default: 720)."
    )
    parser.add_argument("--fps", type=int, default=15, help="The framerate of the camera (default: 15).")
    parser.add_argument(
        "--capture-dir",
        type=str,
        default=str(Path.home() / "curious_frame_captures"),
        help="The directory to store captures (default: ~/curious_frame_captures).",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default="hf.co/unsloth/gemma-3n-E2B-it-GGUF:Q4_K_M",
        help="The name of the language model to use (default: hf.co/unsloth/gemma-3n-E2B-it-GGUF:Q4_K_M).",
    )
    parser.add_argument(
        "--vlm-model",
        type=str,
        default="vikhyatk/moondream2",
        help="The name of the vision model to use (default: vikhyatk/moondream2).",
    )
    parser.add_argument(
        "--vlm-revision",
        type=str,
        default="2025-06-21",
        help="The revision of the vision model (default: 2025-06-21).",
    )
    parser.add_argument(
        "--ollama-url",
        type=str,
        default="http://127.0.0.1:11434/api/chat",
        help="The URL of the Ollama API (default: http://127.0.0.1:11434/api/chat).",
    )
    parser.add_argument(
        "--piper-url",
        type=str,
        default="http://127.0.0.1:5000",
        help="The URL of the Piper TTS API (default: http://127.0.0.1:5000).",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        choices=["en", "fr"],
        help="The default language to use (default: en).",
    )
    args = parser.parse_args()

    camera = Camera(
        camera_id=args.camera_id, width=args.width, height=args.height, fps=args.fps
    )
    vision = Vision(model_name=args.vlm_model, revision=args.vlm_revision)
    language = Language(model=args.llm_model, url=args.ollama_url)
    audio = Audio(piper_url=args.piper_url, language_model=language, language=args.language)

    # Create a directory to store the captures
    capture_dir = Path(args.capture_dir)
    capture_dir.mkdir(parents=True, exist_ok=True)
    csv_path = capture_dir / "captures.csv"

    audio.speak("Hey there! I am curious about the world around me. Let's explore together!")

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        # Save the image first
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = capture_dir / f"{timestamp}.jpg"
        camera.save_frame(str(image_path), frame)

        objects = None
        description = None
        objects_list = None
        try:
            # audio.speak("I am looking for objects.")
            objects_list = vision.find_objects(frame)
            found_flag = False

            if objects_list is not None:
                objects = []
                for obj in objects_list.split(","):
                    obj = obj.strip()
                    if obj:
                        if obj.lower() != "french flag":
                            objects.append(obj)
                        else:
                            found_flag = True
                            if audio.language != "fr":
                                audio.set_language("fr")
                                audio.speak("Je vais maintenant parler en français.")
                
                if not found_flag and audio.language != "en":
                    audio.set_language("en")
                    audio.speak("I'm switching to English.")

                if objects:
                    object_str = ", ".join(objects)
                    audio.speak(f"I found {object_str}, let me think about it.")
                    description = language.chat(object_str)
                    print(f"Description: {description}")
                    audio.speak(description)
                elif found_flag:
                    # This case happens when only the french flag is detected
                    description = language.chat("the French flag")
                    print(f"Description: {description}")
                    audio.speak(description)

            else:
                audio.speak("I could not find any objects.")
                print("No objects found.")
                objects = "N/A"
        except Exception as e:
            audio.speak("I don't know what to say, sorry.")
            print(f"An error occurred: {e}")
            description = f"Error: {e}"

        # Always store the information in the CSV file
        with open(csv_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    str(image_path),
                    objects_list if objects_list else "N/A",
                    description if description else "N/A",
                ]
            )

        break
    camera.release()


if __name__ == "__main__":
    main()
