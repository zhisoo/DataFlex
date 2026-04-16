
# DataFlex

<p align="center">
 Data Select · Mix · Reweight — Right in the LLM Training Loop
  <img src="https://github.com/user-attachments/assets/12b542ed-3cd9-43a9-acf0-8ebcfe564ecd" width="90%">
</p>
<div align="center">

[![Documents](https://img.shields.io/badge/Documents-Click_here-brightgreen?logo=read-the-docs)](https://OpenDCAI.github.io/DataFlex-Doc/)
[![](https://img.shields.io/github/license/OpenDCAI/DataFlex)](https://github.com/OpenDCAI/DataFlex/blob/main/LICENSE)
[![](https://img.shields.io/github/stars/OpenDCAI/DataFlex?style=social)](https://github.com/OpenDCAI/DataFlex)
[![](https://img.shields.io/github/contributors/OpenDCAI/DataFlex)](https://github.com/OpenDCAI/DataFlex/graphs/contributors)
[![](https://img.shields.io/github/repo-size/OpenDCAI/DataFlex?color=green)](https://github.com/OpenDCAI/DataFlex)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/OpenDCAI/DataFlex)

<!-- [![](https://img.shields.io/github/last-commit/OpenDCAI/DataFlex)](https://github.com/OpenDCAI/DataFlex/commits/main/) -->
<!--[![](https://img.shields.io/github/issues-raw/OpenDCAI/DataFlex)](https://github.com/OpenDCAI/DataFlex/issues) -->

🎉 If you like our project, please give us a star ⭐ on GitHub for the latest update.

[简体中文](./README-zh.md) | English

</div>

> **Personal fork note:** I'm using this repo to experiment with data reweighting strategies for fine-tuning smaller models (7B range). My notes and experiment configs are in the `experiments/` folder.

## 📰 1. News
- [2026-04-04] 🎉 Our [technical report](https://huggingface.co/papers/2603.26164) ranked #1 on the Hugging Face Daily Papers leaderboard for that day.
- [2026-03-17] We now support gradient computation under DeepSpeed ZeRO-3, enabling training and analysis of larger-scale models.
- [2025-12-23] 🎉 We're excited to announce the first Data-Centric Training System DataFlex, is now released! Stay tuned for future updates.


## 🔍 2. Overview
<img src="https://github.com/user-attachments/assets/093bfc8e-f450-4048-ad22-456edfdc00d9">

**DataFlex** is an advanced dynamic training framework built on top of [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory).  
It intelligently schedules training data during optimization and integrates several difficult-to-reproduce repositories into a unified framework. The system provides reproducible implementations of **Data Selection**, **Data Mixture**, and **Data Reweighting**, thereby improving both experimental reproducibility and final model performance.

DataFlex integrates seamlessly with LLaMA-Factory, offering researchers and developers more flexible and powerful training control. For goals and design philosophy, please refer to [DataFlex-Doc](https://opendcai.github.io/DataFlex-Doc/).
We summarize repositories related to Data Selection, Data Mixture, and Data Reweighting.
❌ indicates that no official repository is available;
✅ indicates that an official repository is available;
⚠️ indicates that an official repository exists but contains issues.

- **Data Selection**: Dynamically selects training samples according to a given strategy (e.g., focus on "hard" samples). The data selection algorithms are summarized 
