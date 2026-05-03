# AI Frame Generation Render for Blender

This repository contains the official implementation of the Blender AI Frame Interpolation pipeline described in our research paper. This tool integrates the **RIFE (Real-Time Intermediate Flow Estimation)** model directly into the Blender rendering workflow to accelerate production times by interpolating intermediate frames.

## 🚀 Features
* **Automated Interpolation:** Automatically triggers RIFE processing after a Blender animation render is complete.
* **Flexible Multipliers:** Support for 2x, 4x, 6x, and 8x frame interpolation.
* **Hardware Optimization:** Manual GPU ID selection to utilize specific dGPUs or fall back to CPU (-1).
* **Seamless Integration:** Native Windows batch execution with automated cleanup of temporary launcher files.

## 🛠️ Installation
1. **Download RIFE:** Ensure you have the `rife-ncnn-vulkan` executable installed on your system.
2. **Install Addon:**
   - Download `addon/AI Frame Generation.py` from this repository.
   - In Blender, go to `Edit > Preferences > Add-ons > Install...` and select the file.
   - Enable the add-on: **Render: AI Frame Generation Render**.

## 📖 Usage
1. Navigate to the **Output Properties** panel in Blender.
2. Locate the **AI Frame Generation** section.
3. Set your **RIFE Executable** path (e.g., `C:\rife-ncnn-vulkan\rife-ncnn-vulkan.exe`).
4. Choose your **Multiplier** and **GPU ID** (0 is typically your primary GPU).
5. Click **Render Animation (AI Pipeline)** to start.

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
