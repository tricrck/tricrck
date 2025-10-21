import os
import json
import math
from datetime import datetime
import svgwrite

class SVGGenerator:
    def __init__(self):
        self.data_dir = 'data'
        self.assets_dir = 'assets'
        os.makedirs(self.assets_dir, exist_ok=True)
        
        # Modern color palette
        self.colors = {
            'primary': '#6366f1',      # Indigo
            'secondary': '#8b5cf6',    # Purple
            'accent': '#ec4899',       # Pink
            'success': '#10b981',      # Green
            'background': '#0f172a',   # Slate 900
            'surface': '#1e293b',      # Slate 800
            'surface_light': '#334155', # Slate 700
            'text': '#f1f5f9',         # Slate 100
            'text_muted': '#94a3b8',   # Slate 400
            'border': '#475569'        # Slate 600
        }
        
        # Load skill data
        with open(f'{self.data_dir}/skills.json', 'r') as f:
            self.skills_data = json.load(f)
    
    def create_skill_bars_svg(self):
        """Generate modern animated skill bars"""
        print("🎨 Creating modern skill visualization...")
        
        # Use dao_paths instead of skills
        skills = dict(sorted(
            self.skills_data['dao_paths'].items(),
            key=lambda x: x[1]['level'],
            reverse=True
        )[:8])
        
        width = 1280
        height = 80 + len(skills) * 70
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/skills.svg',
            size=(width, height),
            profile='full'
        )
        
        # Modern styles with smooth animations
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            .title { 
                fill: #f1f5f9; 
                font-family: 'Inter', sans-serif; 
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            .subtitle { 
                fill: #94a3b8; 
                font-family: 'Inter', sans-serif; 
                font-size: 14px;
                font-weight: 400;
            }
            .skill-name { 
                fill: #f1f5f9; 
                font-family: 'Inter', sans-serif; 
                font-size: 16px; 
                font-weight: 600;
            }
            .skill-meta { 
                fill: #94a3b8; 
                font-family: 'Inter', sans-serif; 
                font-size: 13px; 
                font-weight: 400;
            }
            .bar-bg { 
                fill: #1e293b;
                rx: 8;
            }
            .bar-fill { 
                fill: url(#skillGradient);
                rx: 8;
                animation: slideIn 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards, pulse 3s ease-in-out infinite;
                transform-origin: left;
            }
            .bar-shine {
                fill: url(#shineGradient);
                rx: 8;
                opacity: 0.4;
            }
            @keyframes slideIn {
                from { 
                    transform: scaleX(0);
                    opacity: 0;
                }
                to { 
                    transform: scaleX(1);
                    opacity: 1;
                }
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.85; }
            }
            .card {
                filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
            }
            .badge {
                fill: #334155;
                rx: 6;
            }
            .badge-text {
                fill: #f1f5f9;
                font-family: 'Inter', sans-serif;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        dwg.add(style)
        
        # Gradients
        gradient = dwg.defs.add(dwg.linearGradient(id="skillGradient", x1="0%", y1="0%", x2="100%", y2="0%"))
        gradient.add_stop_color(0, '#6366f1')
        gradient.add_stop_color(0.5, '#8b5cf6')
        gradient.add_stop_color(1, '#ec4899')
        
        shine = dwg.defs.add(dwg.linearGradient(id="shineGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        shine.add_stop_color(0, '#ffffff', opacity=0.2)
        shine.add_stop_color(0.5, '#ffffff', opacity=0)
        shine.add_stop_color(1, '#000000', opacity=0.1)
        
        # Background with gradient
        bg_gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        bg_gradient.add_stop_color(0, '#0f172a')
        bg_gradient.add_stop_color(1, '#1e293b')
        
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill='url(#bgGradient)'
        ))
        
        # Header
        dwg.add(dwg.text(
            'Dao Paths & Cultivation',
            insert=(50, 45),
            class_='title'
        ))
        
        dwg.add(dwg.text(
            'Programming languages ranked by cultivation level',
            insert=(50, 68),
            class_='subtitle'
        ))
        
        # Skill bars
        y_offset = 110
        bar_width = 550
        bar_height = 32
        
        for idx, (skill_name, data) in enumerate(skills.items()):
            level = data['level']
            mastery_percentage = data['mastery_percentage']
            qi = data['qi']
            
            # Card background
            card_padding = 20
            card_width = width - 100
            card_height = 50
            
            # Skill name and badge
            dwg.add(dwg.text(
                skill_name,
                insert=(70, y_offset + 22),
                class_='skill-name'
            ))
            
            # Level badge
            badge_x = 70 + len(skill_name) * 9 + 10
            dwg.add(dwg.rect(
                insert=(badge_x, y_offset + 9),
                size=(40, 20),
                class_='badge'
            ))
            dwg.add(dwg.text(
                f"L{level}",
                insert=(badge_x + 20, y_offset + 22),
                text_anchor='middle',
                class_='badge-text'
            ))
            
            # Background bar
            bar_x = 320
            dwg.add(dwg.rect(
                insert=(bar_x, y_offset + 3),
                size=(bar_width, bar_height),
                class_='bar-bg'
            ))
            
            # Progress bar with animation delay
            progress_width = (level / 99) * bar_width
            bar = dwg.rect(
                insert=(bar_x, y_offset + 3),
                size=(progress_width, bar_height),
                class_='bar-fill'
            )
            bar['style'] = f'animation-delay: {idx * 0.1}s;'
            dwg.add(bar)
            
            # Shine overlay
            dwg.add(dwg.rect(
                insert=(bar_x, y_offset + 3),
                size=(progress_width, bar_height),
                class_='bar-shine'
            ))
            
            # Qi and mastery text
            dwg.add(dwg.text(
                f'{mastery_percentage}% mastery | {qi} Qi',
                insert=(bar_x + bar_width + 20, y_offset + 24),
                class_='skill-meta'
            ))
            
            y_offset += 60
        
        # Footer
        footer_y = height - 25
        dwg.add(dwg.text(
            f'Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M")}',
            insert=(width/2, footer_y),
            text_anchor='middle',
            class_='subtitle'
        ))
        
        dwg.save()
        print("✅ Modern skill bars generated!")
    
    def create_elemental_affinities_svg(self):
        """Generate elemental affinities visualization"""
        print("🌌 Creating elemental affinities visualization...")
        
        width = 1000
        height = 600
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/elemental_affinities.svg',
            size=(width, height),
            profile='full'
        )
        
        # Styles
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            .title { 
                fill: #f1f5f9; 
                font-family: 'Inter', sans-serif; 
                font-size: 28px;
                font-weight: 700;
            }
            .element-title { 
                fill: #f1f5f9; 
                font-family: 'Inter', sans-serif; 
                font-size: 20px;
                font-weight: 600;
            }
            .element-desc { 
                fill: #94a3b8; 
                font-family: 'Inter', sans-serif; 
                font-size: 14px;
            }
            .language-name { 
                fill: #f1f5f9; 
                font-family: 'Inter', sans-serif; 
                font-size: 14px;
                font-weight: 600;
            }
            .language-meta { 
                fill: #94a3b8; 
                font-family: 'Inter', sans-serif; 
                font-size: 12px;
            }
            .element-card {
                fill: #1e293b;
                rx: 12;
                transition: all 0.3s ease;
            }
            .element-card:hover {
                fill: #334155;
                transform: translateY(-2px);
            }
        """)
        dwg.add(style)
        
        # Background
        bg_gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        bg_gradient.add_stop_color(0, '#0f172a')
        bg_gradient.add_stop_color(1, '#1e293b')
        
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill='url(#bgGradient)'
        ))
        
        # Title
        dwg.add(dwg.text(
            'Elemental Affinities',
            insert=(50, 45),
            class_='title'
        ))
        
        dwg.add(dwg.text(
            'Programming languages grouped by elemental alignment',
            insert=(50, 68),
            class_='subtitle'
        ))
        
        # Element colors
        element_colors = {
            'yang': '#f59e0b',  # Amber
            'yin': '#8b5cf6',   # Purple
            'metal': '#6b7280', # Gray
            'void': '#06b6d4'   # Cyan
        }
        
        # Layout elements in a grid
        elements = list(self.skills_data['elemental_affinities'].items())
        card_width = 450
        card_height = 200
        margin = 30
        
        for idx, (element_key, element_data) in enumerate(elements):
            row = idx // 2
            col = idx % 2
            
            x = 50 + col * (card_width + margin)
            y = 100 + row * (card_height + margin)
            
            # Element card
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(card_width, card_height),
                class_='element-card'
            ))
            
            # Element title
            dwg.add(dwg.text(
                element_data['title'],
                insert=(x + 20, y + 35),
                class_='element-title'
            ))
            
            # Element description
            dwg.add(dwg.text(
                element_data['element'],
                insert=(x + 20, y + 55),
                class_='element-desc'
            ))
            
            # Languages in this element
            languages = list(element_data['paths'].items())[:4]  # Top 4 languages
            lang_y = y + 85
            
            for lang_idx, (lang_name, lang_data) in enumerate(languages):
                dwg.add(dwg.text(
                    f"{lang_name} - L{lang_data['level']}",
                    insert=(x + 30, lang_y + lang_idx * 25),
                    class_='language-name'
                ))
                
                dwg.add(dwg.text(
                    f"{lang_data['mastery_percentage']}% mastery | {lang_data['qi']} Qi",
                    insert=(x + 30, lang_y + lang_idx * 25 + 15),
                    class_='language-meta'
                ))
        
        # Footer
        footer_y = height - 25
        dwg.add(dwg.text(
            f'Total Dao Paths: {self.skills_data["immortal_stats"]["total_dao_paths"]} | Average Level: {self.skills_data["immortal_stats"]["average_dao_level"]}',
            insert=(width/2, footer_y),
            text_anchor='middle',
            class_='subtitle'
        ))
        
        dwg.save()
        print("✅ Elemental affinities visualization generated!")
    
    def create_cultivation_stats_svg(self):
        """Generate cultivation statistics visualization"""
        print("📊 Creating cultivation stats visualization...")
        
        width = 800
        height = 400
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/cultivation_stats.svg',
            size=(width, height),
            profile='full'
        )
        
        # Styles
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            .title { 
                fill: #f1f5f9; 
                font-family: 'Inter', sans-serif; 
                font-size: 28px;
                font-weight: 700;
            }
            .stat-value { 
                fill: #6366f1; 
                font-family: 'Inter', sans-serif; 
                font-size: 36px;
                font-weight: 700;
            }
            .stat-label { 
                fill: #94a3b8; 
                font-family: 'Inter', sans-serif; 
                font-size: 14px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .stat-card {
                fill: #1e293b;
                rx: 12;
                transition: all 0.3s ease;
            }
            .stat-card:hover {
                fill: #334155;
            }
            .progress-bg {
                fill: #1e293b;
                rx: 10;
            }
            .progress-fill {
                fill: url(#progressGradient);
                rx: 10;
            }
        """)
        dwg.add(style)
        
        # Background
        bg_gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        bg_gradient.add_stop_color(0, '#0f172a')
        bg_gradient.add_stop_color(1, '#1e293b')
        
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill='url(#bgGradient)'
        ))
        
        # Progress gradient
        progress_gradient = dwg.defs.add(dwg.linearGradient(id="progressGradient", x1="0%", y1="0%", x2="100%", y2="0%"))
        progress_gradient.add_stop_color(0, '#6366f1')
        progress_gradient.add_stop_color(1, '#8b5cf6')
        
        # Title
        dwg.add(dwg.text(
            'Cultivation Statistics',
            insert=(50, 45),
            class_='title'
        ))
        
        # Main stats
        stats = self.skills_data['immortal_stats']
        heavenly = self.skills_data['heavenly_records']
        
        # Stat cards layout
        card_width = 180
        card_height = 100
        margin = 20
        
        stats_data = [
            ("Total Qi", f"{stats['total_qi']}", "Cultivation Energy"),
            ("Cultivation Level", f"{stats['immortal_level']}", f"{stats['cultivation_realm']}"),
            ("Dao Paths", f"{stats['total_dao_paths']}", "Languages Mastered"),
            ("Strongest Dao", f"L{stats['strongest_dao_level']}", "Highest Level"),
            ("Enlightenments", f"{heavenly['total_enlightenments']}", "Total Projects"),
            ("Created Artifacts", f"{heavenly['created_artifacts']}", "Repositories")
        ]
        
        for idx, (label, value, sublabel) in enumerate(stats_data):
            row = idx // 3
            col = idx % 3
            
            x = 50 + col * (card_width + margin)
            y = 80 + row * (card_height + margin)
            
            # Stat card
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(card_width, card_height),
                class_='stat-card'
            ))
            
            # Stat value
            dwg.add(dwg.text(
                value,
                insert=(x + card_width/2, y + 45),
                text_anchor='middle',
                class_='stat-value'
            ))
            
            # Stat label
            dwg.add(dwg.text(
                label,
                insert=(x + card_width/2, y + 70),
                text_anchor='middle',
                class_='stat-label'
            ))
            
            # Stat sublabel
            dwg.add(dwg.text(
                sublabel,
                insert=(x + card_width/2, y + 85),
                text_anchor='middle',
                class_='subtitle'
            ))
        
        # Cultivation progress bar
        progress_y = 350
        progress_width = 700
        progress_height = 20
        
        dwg.add(dwg.rect(
            insert=(50, progress_y),
            size=(progress_width, progress_height),
            class_='progress-bg'
        ))
        
        # Calculate progress based on level (6/99)
        progress_percent = (stats['immortal_level'] / 99) * progress_width
        dwg.add(dwg.rect(
            insert=(50, progress_y),
            size=(progress_percent, progress_height),
            class_='progress-fill'
        ))
        
        # Progress text
        dwg.add(dwg.text(
            f"Cultivation Progress: {stats['immortal_level']}/99 ({stats['immortal_level']/99*100:.1f}%)",
            insert=(50 + progress_width/2, progress_y - 10),
            text_anchor='middle',
            class_='subtitle'
        ))
        
        dwg.save()
        print("✅ Cultivation stats visualization generated!")

    def generate_all_visualizations(self):
        """Generate all visualizations"""
        self.create_skill_bars_svg()
        self.create_elemental_affinities_svg()
        self.create_cultivation_stats_svg()
        print("🎉 All visualizations completed!")

def main():
    print("=" * 50)
    print("   Modern SVG Visualization Generator")
    print("=" * 50 + "\n")
    
    try:
        generator = SVGGenerator()
        generator.generate_all_visualizations()
        
        print("\n" + "=" * 50)
        print("   ✨ Success! Visualizations ready")
        print("=" * 50)
        
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())