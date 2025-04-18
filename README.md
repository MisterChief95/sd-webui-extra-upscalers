# SD Forge Extra Upscalers

This extension for [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)/[Stable Diffusion Web UI Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge) adds support for additional upscalers via [Spandrel](https://github.com/chaiNNer-org/spandrel).

## Supported Upscalers

- **ATD**
- **DRCT**
- **MoSR** (requires `spandrel >= 0.4.0`)
- **MoESR** (requires `spandrel >= 0.4.1`)
- **PLKSR**
- **RealPLKSR**
- **RCAN** (requires `spandrel >= 0.4.1`)

## Installation

1. Copy or clone this extension into your `extensions/` directory of SD Web UI Forge.
2. Restart the Web UI.

## Usage

- The new upscalers will appear in the upscaler selection menu.
- Select your desired upscaler and process images as usual.

## Configuration

#### Settings

Adds options to the `Upscaler` settings section to tweak tile size & overlap for each upscaling model.

#### Model Paths

You can set the directory path for each model type individual through command line args. Example:

```shell
--atd-models-path "./models/new_atd_directory"
```

Just follow the same pattern of `--<model_type>-models-path` and make sure its all lowercase. Only use forward slashes (`/`) in directory paths.

## Notes

- Ensure you have the correct version of Spandrel for all upscalers to function.
- For MoSR, MoESR, and RCAN, check the version requirements above.

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

```
http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
