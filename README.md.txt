# AI Frame Generation Render for Blender

This repository contains the official implementation of the Blender AI Frame Interpolation pipeline described in our research paper. This tool integrates the **RIFE (Real-Time Intermediate Flow Estimation)** model directly into the Blender rendering workflow to accelerate production times by interpolating intermediate frames.

## 🚀 Features
* **Automated Interpolation:** Automatically triggers RIFE processing after a Blender animation render is complete.
* **Flexible Multipliers:** Support for 2x, 4x, 6x, and 8x frame interpolation[cite: 1].
* **Hardware Optimization:** Manual GPU ID selection to utilize specific dGPUs or fall back to CPU (-1)[cite: 1].
* **Seamless Integration:** Native Windows batch execution with automated cleanup of temporary launcher files[cite: 1].

## 🛠️ Installation
1. **Download RIFE:** Ensure you have the `rife-ncnn-vulkan` executable installed on your system[cite: 1].
2. **Install Addon:**
   - Download `addon/AI Frame Generation.py` from this repository[cite: 1].
   - In Blender, go to `Edit > Preferences > Add-ons > Install...` and select the file[cite: 1].
   - Enable the add-on: **Render: AI Frame Generation Render**[cite: 1].

## 📖 Usage
1. Navigate to the **Output Properties** panel in Blender[cite: 1].
2. Locate the **AI Frame Generation** section[cite: 1].
3. Set your **RIFE Executable** path (e.g., `C:\rife-ncnn-vulkan\rife-ncnn-vulkan.exe`)[cite: 1].
4. Choose your **Multiplier** and **GPU ID** (0 is typically your primary GPU)[cite: 1].
5. Click **Render Animation (AI Pipeline)** to start[cite: 1].

## 📝 Citation
If you use this code in your research, please cite our paper:
> *Author(s), "Title of your Research Paper," Journal/Conference Name, Year.*

## ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.