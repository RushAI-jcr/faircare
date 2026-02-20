"""
Visualization Constants for FairCareAI.

This module contains magic numbers and constants used throughout the
visualization modules, extracted for clarity and maintainability.
"""

# =============================================================================
# COLOR SCIENCE CONSTANTS
# =============================================================================

# sRGB luminance weights (ITU-R BT.709 standard)
# Used for calculating relative luminance of colors
SRGB_RED_WEIGHT = 0.2126
SRGB_GREEN_WEIGHT = 0.7152
SRGB_BLUE_WEIGHT = 0.0722

# sRGB gamma correction constants
# Used for linearizing sRGB color values
SRGB_GAMMA_THRESHOLD = 0.03928
SRGB_GAMMA_COEFFICIENT = 1.055
SRGB_GAMMA_EXPONENT = 2.4

# WCAG 2.1 contrast ratio thresholds
WCAG_AA_NORMAL_TEXT_RATIO = 4.5  # For regular text (< 18pt or < 14pt bold)
WCAG_AA_LARGE_TEXT_RATIO = 3.0  # For large text (>= 18pt or >= 14pt bold)
WCAG_AAA_NORMAL_TEXT_RATIO = 7.0  # Enhanced contrast for regular text
WCAG_AAA_LARGE_TEXT_RATIO = 4.5  # Enhanced contrast for large text

# Minimum contrast ratio for UI elements (WCAG 2.1 Level AA)
WCAG_MIN_UI_CONTRAST = 3.0

# =============================================================================
# CHART LAYOUT CONSTANTS
# =============================================================================

# Chart positioning and spacing
CHART_ANNOTATION_Y_OFFSET = -0.12  # Vertical offset for source annotations
CHART_LEGEND_ORIENTATION_THRESHOLD = 1.02  # Aspect ratio threshold for vertical legend

# Font sizes (in points)
TITLE_FONT_SIZE = 24
SUBTITLE_FONT_SIZE = 16
AXIS_TITLE_FONT_SIZE = 14
AXIS_LABEL_FONT_SIZE = 12
LEGEND_FONT_SIZE = 12
ANNOTATION_FONT_SIZE = 10
SOURCE_NOTE_FONT_SIZE = 9

# Chart dimensions (in pixels)
DEFAULT_CHART_WIDTH = 1200
DEFAULT_CHART_HEIGHT = 800
DEFAULT_DASHBOARD_WIDTH = 1400
DEFAULT_DASHBOARD_HEIGHT = 1000
