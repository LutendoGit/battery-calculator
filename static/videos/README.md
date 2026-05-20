# Video Learning Materials

This directory contains video learning materials for the WattWorks education platform.

## How to Add Videos

### Option 1: Local Video Files
1. **Upload video files** to this directory (static/videos/)
   - Supported formats: MP4, WebM, OGV
   - Recommended: MP4 for best browser compatibility
   - File size limit: Keep under 100MB for web performance

2. **Update the educational content** in `modules/lithium_education.py`:
   ```python
   "videos": [
       {
           "title": "Your Video Title",
           "url": "/static/videos/your-video-filename.mp4",
           "description": "Brief description of what the video covers",
           "duration": "MM:SS"  # Optional
       }
   ]
   ```

### Option 2: External Video Hosting (YouTube, Vimeo, etc.)

1. **Get the video URL** from the platform
   - YouTube: Regular URL (https://www.youtube.com/watch?v=VIDEO_ID)
   - YouTube: Short URL (https://youtu.be/VIDEO_ID)
   - Vimeo: Video URL (https://vimeo.com/VIDEO_ID)

2. **Add to educational content**:
   ```python
   "videos": [
       {
           "title": "Battery Installation Safety",
           "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
           "description": "Essential safety procedures for battery installation",
           "duration": "8:45"
       },
       {
           "title": "Solar Panel Maintenance",
           "url": "https://youtu.be/example-video-id",
           "description": "How to maintain solar panels for optimal performance",
           "duration": "12:30"
       }
   ]
   ```

3. **Automatic embed conversion**: The system automatically converts YouTube URLs to embed format

## Supported External Platforms

- **YouTube**: Full support with automatic embed URL conversion
- **Vimeo**: Direct embed URL support
- **Other platforms**: Use direct embed URLs if available

## Video Best Practices

- **Keep videos under 10 minutes** for better engagement
- **Use clear audio and good lighting**
- **Include captions/subtitles** when possible
- **Test on multiple devices** and browsers

## Current Videos

### Local Videos
- `power-vs-energy.mp4` - Explains the difference between power (kW) and energy (kWh)
- `ac-vs-dc-explained.mp4` - AC vs DC power in solar systems
- `how-lithium-batteries-work.mp4` - Lithium-ion battery chemistry animation

### External Videos
- YouTube videos are automatically embedded

## Hosting Options

For larger video libraries, consider:
- **YouTube/Vimeo**: Free hosting with embed support
- **Cloud storage**: AWS S3, Google Cloud Storage
- **CDN**: For faster delivery worldwide
- **Streaming services**: Better performance for long videos

## Technical Notes

- **Local videos**: Served directly from Flask static folder using HTML5 video player
- **External videos**: Embedded using iframe with privacy-enhanced mode
- **Responsive design**: Adapts to screen size
- **Fallback support**: Graceful degradation for unsupported browsers
- **Progress tracking**: All videos count toward lesson completion