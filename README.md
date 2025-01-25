<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/animationem/prism-discord/blob/main/Resources/prism_discord_logo_long_light_banner.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/animationem/prism-discord/blob/main/Resources/prism_discord_logo_long_dark_banner.svg">
  <img alt="Prism and discord branding" src="https://github.com/animationem/prism-discord/tree/main/Resources/prism_discord_logo_long_light_banner.svg">
</picture>  
  
<div>
<img src="https://img.shields.io/badge/Prism_Pipeline-2.0.14-mediumseagreen" alt="Prism Pipeline Version"> 
<img src="https://img.shields.io/badge/discord_Plugin-2.0.14-4A154B?logo=discord" alt="Discord Plugin Version">
</div>  
<br>
  
> [!IMPORTANT]  
> Documentation Coming Soon
  
    
## Table of Contents  
1. [Introduction](#introduction)
2. [Requirements](#requirements)
    1. [discord](#requirements-discord)
3. [Installation](#installation)
    1. [Prism - Install Plugin](#plugin)
4. [Known Bugs/Limitations](#known-bugs-and-limitations)

## Introduction

This is the Discord plugin for Prism-Pipeline 2.0

## Requirements

### Discord

1. Discord Bot

   - You are required to create a Discord bot for this plugin. You can find the installation process for this below or check the documentation here: [Documentation Coming Soon]

2. Channel Name = Project Name
   - Your channel must match the name of your current project. Will add the option for a custom Discord channel in the future

## Installation

### Plugin

1. Download the Plugin

> Option 1: Download the current release package from the repository's release page.

    Option 2: Download the repository as a ZIP file using the Code dropdown menu on the main repository page.

2.Unzip the File (if needed)

> If you downloaded the ZIP file, extract its contents to a folder.

3.  Move the Plugin to the Prism Plugin Folder

    > Locate your Prism Plugin folder.

        Drag and drop the downloaded or unzipped plugin folder into the Prism Plugin folder.

4.  Reload Prism

> Restart or reload Prism.

    The Slack plugin should automatically appear in the plugin list and be checked as enabled.

## Known Bugs and Limitations

<details>
    <summary>Deadline Unsupported</summary>
    Currently publishing to the farm is unsupported. It will need a separate Python task as part of the job in order to carry out the publishing via render farm.
</details>
