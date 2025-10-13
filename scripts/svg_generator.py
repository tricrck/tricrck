#!/usr/bin/env python3
"""
🎨 Cursed SVG Visualization Generator
Creates animated SVG visualizations with gothic aesthetics
"""

import os
import json
from datetime import datetime
import svgwrite
from svgwrite import cm, mm

class SVGNecromancer:
    def __init__(self):
        self.data_dir = 'data'
        self.assets_dir = 'assets'
        os.makedirs(self.assets_dir, exist_ok=True)
        
        # Gothic color scheme
        self.colors = {
            'blood_red': '#8B0000',
            'dark_red': '#4A0000',
            'crimson': '#DC143C',
            'black': '#0a0a0a',
            'dark_gray': '#1a1a1a',
            'gray': '#2a2a2a',
            'bone': '#F5F5DC',
            'shadow': '#1C1C1C'
        }
        
        # Load skill data
        with open(f'{self.data_dir}/skills.json', 'r') as f:
            self.skills_data = json.load(f)
        
        with open(f'{self.data_dir}/github_data.json', 'r') as f:
            self.github_data = json.load(f)
    
    def create_skill_bars_svg(self):
        """Generate animated skill bars SVG"""
        print("🎨 Forging skill visualization...")
        
        skills = dict(sorted(
            self.skills_data['skills'].items(),
            key=lambda x: x[1]['level'],
            reverse=True
        )[:8])  # Top 8 skills
        
        width = 800
        height = 60 + len(skills) * 55
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/skills.svg',
            size=(width, height),
            profile='full'
        )
        
        # Add styles
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Creepster&family=Metal+Mania&display=swap');
            .skill-title { 
                fill: #8B0000; 
                font-family: 'Metal Mania', cursive; 
                font-size: 24px;
                text-shadow: 2px 2px 4px #000;
            }
            .skill-name { 
                fill: #F5F5DC; 
                font-family: 'Courier New', monospace; 
                font-size: 14px; 
                font-weight: bold;
            }
            .skill-level { 
                fill: #DC143C; 
                font-family: 'Courier New', monospace; 
                font-size: 12px; 
            }
            .bar-bg { fill: #1a1a1a; stroke: #4A0000; stroke-width: 1; }
            .bar-fill { 
                fill: url(#bloodGradient); 
                animation: pulse 2s ease-in-out infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 0.8; }
                50% { opacity: 1; }
            }
            .glow {
                filter: drop-shadow(0 0 8px #8B0000);
            }
        """)
        dwg.add(style)
        
        # Add gradient
        gradient = dwg.defs.add(dwg.linearGradient(id="bloodGradient"))
        gradient.add_stop_color(0, '#4A0000')
        gradient.add_stop_color(0.5, '#8B0000')
        gradient.add_stop_color(1, '#DC143C')
        
        # Background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill=self.colors['black']
        ))
        
        # Title
        dwg.add(dwg.text(
            '⚔️ DARK SKILLS GRIMOIRE ⚔️',
            insert=(width/2, 35),
            text_anchor='middle',
            class_='skill-title glow'
        ))
        
        # Draw skill bars
        y_offset = 70
        bar_width = 500
        bar_height = 25
        
        for skill_name, data in skills.items():
            level = data['level']
            percentage = data['percentage']
            rank = data['rank']
            
            # Skill name
            dwg.add(dwg.text(
                skill_name,
                insert=(50, y_offset + 18),
                class_='skill-name'
            ))
            
            # Background bar
            dwg.add(dwg.rect(
                insert=(200, y_offset),
                size=(bar_width, bar_height),
                class_='bar-bg'
            ))
            
            # Progress bar
            progress_width = (level / 99) * bar_width
            dwg.add(dwg.rect(
                insert=(200, y_offset),
                size=(progress_width, bar_height),
                class_='bar-fill'
            ))
            
            # Level text
            level_text = f"Level {level} | {rank} | {percentage}%"
            dwg.add(dwg.text(
                level_text,
                insert=(710, y_offset + 18),
                class_='skill-level'
            ))
            
            y_offset += 45
        
        # Footer
        dwg.add(dwg.text(
            f'Last Ritual: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            insert=(width/2, height - 15),
            text_anchor='middle',
            class_='skill-level'
        ))
        
        dwg.save()
        print("✅ Skill bars SVG generated!")
    
    def create_contribution_svg(self):
        """Generate animated contribution calendar"""
        print("📊 Creating dark contribution chart...")
        
        width = 800
        height = 200
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/contributions.svg',
            size=(width, height),
            profile='full'
        )
        
        # Add styles
        style = dwg.style("""
            .contribution-title { 
                fill: #8B0000; 
                font-family: 'Metal Mania', cursive; 
                font-size: 20px;
                text-shadow: 2px 2px 4px #000;
            }
            .contribution-cell { 
                fill: #1a1a1a; 
                stroke: #4A0000; 
                stroke-width: 1;
                animation: glow 3s ease-in-out infinite alternate;
            }
            @keyframes glow {
                from { opacity: 0.7; }
                to { opacity: 1; }
            }
        """)
        dwg.add(style)
        
        # Background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill=self.colors['black']
        ))
        
        # Title
        dwg.add(dwg.text(
            '🌙 CONTRIBUTION NECROMANCY CALENDAR 🌙',
            insert=(width/2, 30),
            text_anchor='middle',
            class_='contribution-title'
        ))
        
        # Generate mock contribution grid
        cell_size = 12
        spacing = 2
        start_x = 50
        start_y = 60
        
        for week in range(20):
            for day in range(7):
                intensity = (week + day) % 4  # Mock data
                color_intensity = 50 + intensity * 50
                color = f'rgb({color_intensity}, 0, 0)'
                
                dwg.add(dwg.rect(
                    insert=(start_x + week * (cell_size + spacing), 
                           start_y + day * (cell_size + spacing)),
                    size=(cell_size, cell_size),
                    fill=color,
                    class_='contribution-cell'
                ))
        
        # Stats
        stats = self.github_data['streaks']
        stats_text = f"Current Streak: {stats['current']} days | Longest: {stats['longest']} days"
        dwg.add(dwg.text(
            stats_text,
            insert=(width/2, height - 20),
            text_anchor='middle',
            class_='skill-level'
        ))
        
        dwg.save()
        print("✅ Contributions SVG generated!")
    
    def create_language_radar(self):
        """Generate radar chart of language skills"""
        print("📈 Creating language radar chart...")
        
        width = 600
        height = 400
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/languages_radar.svg',
            size=(width, height),
            profile='full'
        )
        
        # Background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill=self.colors['black']
        ))
        
        center_x, center_y = width/2, height/2
        max_radius = 150
        
        # Radar grid
        for i in range(1, 6):
            radius = (i / 5) * max_radius
            dwg.add(dwg.circle(
                center=(center_x, center_y),
                r=radius,
                fill='none',
                stroke=self.colors['dark_red'],
                stroke_width=1,
                opacity=0.3
            ))
        
        # Get top languages
        languages = list(self.skills_data['skills'].keys())[:6]
        if len(languages) < 3:
            languages.extend(['Python', 'JavaScript', 'TypeScript', 'Go', 'Rust'])[:6-len(languages)]
        
        # Draw radar points
        for i, lang in enumerate(languages):
            angle = (2 * 3.14159 * i) / len(languages)
            skill_data = self.skills_data['skills'].get(lang, {'level': 10})
            radius = (skill_data['level'] / 99) * max_radius
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            # Connection line
            if i > 0:
                prev_angle = (2 * 3.14159 * (i-1)) / len(languages)
                prev_skill = self.skills_data['skills'].get(languages[i-1], {'level': 10})
                prev_radius = (prev_skill['level'] / 99) * max_radius
                prev_x = center_x + prev_radius * math.cos(prev_angle)
                prev_y = center_y + prev_radius * math.sin(prev_angle)
                
                dwg.add(dwg.line(
                    start=(prev_x, prev_y),
                    end=(x, y),
                    stroke=self.colors['crimson'],
                    stroke_width=2
                ))
            
            # Language point
            dwg.add(dwg.circle(
                center=(x, y),
                r=5,
                fill=self.colors['blood_red']
            ))
            
            # Language label
            dwg.add(dwg.text(
                lang,
                insert=(x + 10, y),
                fill=self.colors['bone'],
                font_size=10
            ))
        
        # Close the polygon
        if len(languages) > 2:
            first_angle = 0
            first_skill = self.skills_data['skills'].get(languages[0], {'level': 10})
            first_radius = (first_skill['level'] / 99) * max_radius
            first_x = center_x + first_radius * math.cos(first_angle)
            first_y = center_y + first_radius * math.sin(first_angle)
            
            last_angle = (2 * 3.14159 * (len(languages)-1)) / len(languages)
            last_skill = self.skills_data['skills'].get(languages[-1], {'level': 10})
            last_radius = (last_skill['level'] / 99) * max_radius
            last_x = center_x + last_radius * math.cos(last_angle)
            last_y = center_y + last_radius * math.sin(last_angle)
            
            dwg.add(dwg.line(
                start=(last_x, last_y),
                end=(first_x, first_y),
                stroke=self.colors['crimson'],
                stroke_width=2
            ))
        
        dwg.add(dwg.text(
            'LANGUAGE MASTERY RADAR',
            insert=(width/2, 30),
            text_anchor='middle',
            class_='skill-title'
        ))
        
        dwg.save()
        print("✅ Language radar SVG generated!")
    
    def generate_all_visualizations(self):
        """Generate all SVG visualizations"""
        self.create_skill_bars_svg()
        self.create_contribution_svg()
        self.create_language_radar()
        print("🎉 All dark visualizations completed!")

import math  # Add this import at the top

def main():
    print("🎨" * 30)
    print("   CURSED SVG GENERATION RITUAL")
    print("🎨" * 30 + "\n")
    
    try:
        necromancer = SVGNecromancer()
        necromancer.generate_all_visualizations()
        
        print("\n" + "🖤" * 30)
        print("   VISUALIZATIONS COMPLETE")
        print("🖤" * 30)
        
        return 0
    except Exception as e:
        print(f"\n💀 RITUAL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())