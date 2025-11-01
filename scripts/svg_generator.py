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
        
        # ENHANCED COLOR PALETTE - Maximum visibility and beauty
        self.colors = {
            # Deep, rich backgrounds
            'bg_primary': '#0a0e27',      # Deep space blue
            'bg_secondary': '#141b2d',    # Slightly lighter
            'bg_card': '#1e293b',         # Card surfaces
            'bg_card_hover': '#334155',   # Hover state
            
            # High-contrast text
            'text_primary': '#f8fafc',    # Near white - maximum visibility
            'text_secondary': '#e2e8f0',  # Slightly dimmer
            'text_muted': '#94a3b8',      # Muted but still readable
            'text_accent': '#fbbf24',     # Gold for emphasis
            
            # Cultivation element colors
            'yang': '#fbbf24',            # Bright gold (Fire/Power)
            'yin': '#a78bfa',             # Light purple (Water/Grace)
            'metal': '#94a3b8',           # Steel blue-gray (System)
            'void': '#22d3ee',            # Bright cyan (Abstract)
            
            # Accent colors
            'accent_primary': '#818cf8',  # Indigo
            'accent_success': '#34d399',  # Emerald
            'accent_danger': '#f87171',   # Red
            
            # Borders
            'border': '#475569',
            'border_bright': '#64748b',
        }
        
        # Load skill data
        with open(f'{self.data_dir}/skills.json', 'r') as f:
            self.skills_data = json.load(f)
    
    def create_skill_bars_svg(self):
        """Generate modern animated skill bars with perfect visibility"""
        print("🎨 Creating cultivation skill visualization...")
        
        skills = dict(sorted(
            self.skills_data['dao_paths'].items(),
            key=lambda x: x[1]['level'],
            reverse=True
        )[:8])
        
        width = 1050
        height = 80 + len(skills) * 70
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/skills.svg',
            size=(width, height),
            profile='full'
        )
        
        # Enhanced styles with maximum visibility
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            .title { 
                fill: #f8fafc;  /* Near-white for maximum visibility */
                font-family: 'Inter', sans-serif; 
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.5px;
            }
            .subtitle { 
                fill: #cbd5e1;  /* Light gray, easily readable */
                font-family: 'Inter', sans-serif; 
                font-size: 15px;
                font-weight: 400;
            }
            .skill-name { 
                fill: #f8fafc;  /* Bright white */
                font-family: 'Inter', sans-serif; 
                font-size: 17px; 
                font-weight: 600;
            }
            .skill-meta { 
                fill: #cbd5e1;  /* Clearly visible metadata */
                font-family: 'Inter', sans-serif; 
                font-size: 14px; 
                font-weight: 500;
            }
            .bar-bg { 
                fill: #1e293b;  /* Dark card background */
                stroke: #334155;  /* Subtle border */
                stroke-width: 1;
                rx: 8;
            }
            .bar-fill { 
                fill: url(#skillGradient);
                rx: 8;
                animation: slideIn 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards, glow 3s ease-in-out infinite;
                transform-origin: left;
            }
            .bar-shine {
                fill: url(#shineGradient);
                rx: 8;
                opacity: 0.5;
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
            @keyframes glow {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.9; }
            }
            .badge {
                fill: #334155;
                stroke: #fbbf24;  /* Gold border */
                stroke-width: 2;
                rx: 6;
            }
            .badge-text {
                fill: #fbbf24;  /* Gold text */
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)
        dwg.add(style)
        
        # Yang energy gradient (Power/Aggression)
        gradient = dwg.defs.add(dwg.linearGradient(id="skillGradient", x1="0%", y1="0%", x2="100%", y2="0%"))
        gradient.add_stop_color(0, '#fbbf24')  # Gold
        gradient.add_stop_color(0.5, '#f59e0b')  # Amber
        gradient.add_stop_color(1, '#ef4444')  # Red
        
        # Shine effect
        shine = dwg.defs.add(dwg.linearGradient(id="shineGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        shine.add_stop_color(0, '#ffffff', opacity=0.3)
        shine.add_stop_color(0.5, '#ffffff', opacity=0)
        shine.add_stop_color(1, '#000000', opacity=0.15)
        
        # Background with atmospheric gradient
        bg_gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        bg_gradient.add_stop_color(0, '#0a0e27')
        bg_gradient.add_stop_color(0.5, '#141b2d')
        bg_gradient.add_stop_color(1, '#1a2332')
        
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill='url(#bgGradient)'
        ))
        
        # Define glow filter
        glow_filter = dwg.defs.add(dwg.filter(id="titleGlow", x="-50%", y="-50%", width="200%", height="200%"))
        glow_filter.feGaussianBlur(in_="SourceAlpha", stdDeviation="4", result="blur")
        glow_filter.feMerge(layernames=['blur', 'SourceGraphic'])
        
        # Header with glow effect
        dwg.add(dwg.text(
            'Dao Paths & Cultivation',
            insert=(width/2, 45),
            text_anchor='middle',
            class_='title',
            filter='url(#titleGlow)'
        ))
        
        dwg.add(dwg.text(
            'Programming languages ranked by cultivation level',
            insert=(width/2, 68),
            text_anchor='middle',
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
            
            # Skill name
            dwg.add(dwg.text(
                skill_name,
                insert=(70, y_offset + 22),
                class_='skill-name'
            ))
            
            # Level badge with golden border
            badge_x = 70 + len(skill_name) * 10 + 10
            dwg.add(dwg.rect(
                insert=(badge_x, y_offset + 9),
                size=(45, 22),
                class_='badge'
            ))
            dwg.add(dwg.text(
                f"L{level}",
                insert=(badge_x + 22, y_offset + 23),
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
            
            # Progress bar
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
            
            # Qi and mastery text - now clearly visible
            dwg.add(dwg.text(
                f'{mastery_percentage}% | {qi:,} Qi',
                insert=(bar_x + bar_width + 20, y_offset + 24),
                class_='skill-meta'
            ))
            
            y_offset += 60
        
        # Footer
        footer_y = height - 25
        dwg.add(dwg.text(
            f'Updated: {datetime.now().strftime("%b %d, %Y")} • Total Cultivation: {self.skills_data["immortal_stats"]["total_qi"]:,} Qi',
            insert=(width/2, footer_y),
            text_anchor='middle',
            class_='subtitle'
        ))
        
        dwg.save()
        print("✅ Cultivation skill bars generated!")
    
    def create_elemental_affinities_svg(self):
        """Generate elemental affinities with distinct element colors"""
        print("🌌 Creating elemental affinities visualization...")
        
        width = 1150
        height = 900
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/elemental_affinities.svg',
            size=(width, height),
            profile='full'
        )
        
        # Styles
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            .title { 
                fill: #f8fafc; 
                font-family: 'Inter', sans-serif; 
                font-size: 32px;
                font-weight: 700;
            }
            .subtitle-main {
                fill: #cbd5e1;
                font-family: 'Inter', sans-serif;
                font-size: 15px;
            }
            .element-title { 
                fill: #f8fafc; 
                font-family: 'Inter', sans-serif; 
                font-size: 22px;
                font-weight: 700;
            }
            .element-desc { 
                fill: #cbd5e1; 
                font-family: 'Inter', sans-serif; 
                font-size: 14px;
                font-weight: 500;
            }
            .language-name { 
                fill: #f8fafc; 
                font-family: 'Inter', sans-serif; 
                font-size: 15px;
                font-weight: 600;
            }
            .language-meta { 
                fill: #94a3b8; 
                font-family: 'Inter', sans-serif; 
                font-size: 13px;
                font-weight: 500;
            }
            .element-card {
                rx: 12;
                stroke-width: 2;
            }
            .element-icon {
                font-size: 28px;
            }
        """)
        dwg.add(style)
        
        # Background
        bg_gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        bg_gradient.add_stop_color(0, '#0a0e27')
        bg_gradient.add_stop_color(1, '#141b2d')
        
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill='url(#bgGradient)'
        ))
        
        # Title
        dwg.add(dwg.text(
            'Elemental Affinities',
            insert=(width/2, 45),
            text_anchor='middle',
            class_='title'
        ))
        
        dwg.add(dwg.text(
            'Programming languages grouped by elemental alignment',
            insert=(width/2, 70),
            text_anchor='middle',
            class_='subtitle-main'
        ))
        
        # Element colors and icons
        element_config = {
            'yang': {
                'color': '#fbbf24',
                'bg': '#1e293b',
                'icon': '☀️',
                'glow': 'rgba(251, 191, 36, 0.2)'
            },
            'yin': {
                'color': '#a78bfa',
                'bg': '#1e293b',
                'icon': '🌙',
                'glow': 'rgba(167, 139, 250, 0.2)'
            },
            'metal': {
                'color': '#94a3b8',
                'bg': '#1e293b',
                'icon': '⚔️',
                'glow': 'rgba(148, 163, 184, 0.2)'
            },
            'void': {
                'color': '#22d3ee',
                'bg': '#1e293b',
                'icon': '🌀',
                'glow': 'rgba(34, 211, 238, 0.2)'
            }
        }
        
        # Layout elements in a grid
        elements = list(self.skills_data['elemental_affinities'].items())
        card_width = 480
        card_height = 320
        margin = 40
        
        for idx, (element_key, element_data) in enumerate(elements):
            row = idx // 2
            col = idx % 2
            
            x = 50 + col * (card_width + margin)
            y = 110 + row * (card_height + margin)
            
            config = element_config.get(element_key, element_config['yang'])
            
            # Element card with colored border
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(card_width, card_height),
                fill=config['bg'],
                stroke=config['color'],
                class_='element-card'
            ))
            
            # Element icon and title
            dwg.add(dwg.text(
                f"{config['icon']} {element_data['title']}",
                insert=(x + 20, y + 40),
                class_='element-title',
                fill=config['color']
            ))
            
            # Element description
            dwg.add(dwg.text(
                element_data['element'],
                insert=(x + 20, y + 65),
                class_='element-desc'
            ))
            
            # Languages in this element
            languages = list(element_data['paths'].items())[:4]
            print(len(languages))
            lang_y = y + 100
            
            for lang_idx, (lang_name, lang_data) in enumerate(languages):
                # Language name with level
                dwg.add(dwg.text(
                    f"• {lang_name} - L{lang_data['level']}",
                    insert=(x + 30, lang_y + lang_idx * len(languages)*15),
                    class_='language-name'
                ))
                
                # Language meta
                dwg.add(dwg.text(
                    f"  {lang_data['mastery_percentage']}% mastery | {lang_data['qi']:,} Qi",
                    insert=(x + 30, lang_y + lang_idx * len(languages)*15 + 26),
                    class_='language-meta'
                ))
        
        # Footer
        stats = self.skills_data["immortal_stats"]
        footer_y = height - 30
        dwg.add(dwg.text(
            f'Total Dao Paths: {stats["total_dao_paths"]} | Average Level: {stats["average_dao_level"]:.1f} | Total Qi: {stats["total_qi"]:,}',
            insert=(width/2, footer_y),
            text_anchor='middle',
            class_='subtitle-main'
        ))
        
        dwg.save()
        print("✅ Elemental affinities visualization generated!")
    
    def create_cultivation_stats_svg(self):
        """Generate cultivation statistics with high visibility"""
        print("📊 Creating cultivation stats visualization...")
        
        width = 1050
        height = 600
        
        dwg = svgwrite.Drawing(
            f'{self.assets_dir}/cultivation_stats.svg',
            size=(width, height),
            profile='full'
        )
        
        # Styles
        style = dwg.style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            .title { 
                fill: #f8fafc; 
                font-family: 'Inter', sans-serif; 
                font-size: 32px;
                font-weight: 700;
            }
            .stat-value { 
                fill: #fbbf24;  /* Gold for emphasis */
                font-family: 'Inter', sans-serif; 
                font-size: 42px;
                font-weight: 700;
            }
            .stat-label { 
                fill: #cbd5e1; 
                font-family: 'Inter', sans-serif; 
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
            }
            .stat-sublabel {
                fill: #94a3b8;
                font-family: 'Inter', sans-serif;
                font-size: 12px;
                font-weight: 500;
            }
            .stat-card {
                fill: #1e293b;
                stroke: #475569;
                stroke-width: 1;
                rx: 12;
            }
            .progress-bg {
                fill: #1e293b;
                stroke: #334155;
                stroke-width: 2;
                rx: 10;
            }
            .progress-fill {
                fill: url(#progressGradient);
                rx: 10;
            }
            .progress-text {
                fill: #f8fafc;
                font-family: 'Inter', sans-serif;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        dwg.add(style)
        
        # Background
        bg_gradient = dwg.defs.add(dwg.linearGradient(id="bgGradient", x1="0%", y1="0%", x2="0%", y2="100%"))
        bg_gradient.add_stop_color(0, '#0a0e27')
        bg_gradient.add_stop_color(1, '#141b2d')
        
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(width, height),
            fill='url(#bgGradient)'
        ))
        
        # Progress gradient
        progress_gradient = dwg.defs.add(dwg.linearGradient(id="progressGradient", x1="0%", y1="0%", x2="100%", y2="0%"))
        progress_gradient.add_stop_color(0, '#fbbf24')
        progress_gradient.add_stop_color(0.5, '#f59e0b')
        progress_gradient.add_stop_color(1, '#ef4444')
        
        # Title
        dwg.add(dwg.text(
            'Cultivation Statistics',
            insert=(width/2, 45),
            text_anchor='middle',
            class_='title'
        ))
        
        # Main stats
        stats = self.skills_data['immortal_stats']
        heavenly = self.skills_data['heavenly_records']
        
        # Stat cards layout
        card_width = 300
        card_height = 120
        margin = 20
        
        stats_data = [
            ("Total Qi", f"{stats['total_qi']:,}", "Cultivation Energy"),
            ("Cultivation", f"L{stats['immortal_level']}", stats['cultivation_realm']),
            ("Dao Paths", f"{stats['total_dao_paths']}", "Languages Mastered"),
            ("Strongest", f"L{stats['strongest_dao_level']}", "Highest Dao Level"),
            ("Projects", f"{heavenly['total_enlightenments']}", "Total Enlightenments"),
            ("Artifacts", f"{heavenly['created_artifacts']}", "Repositories Created")
        ]
        
        for idx, (label, value, sublabel) in enumerate(stats_data):
            row = idx // 3
            col = idx % 3
            
            x = 50 + col * (card_width + margin)
            y = 100 + row * (card_height + margin)
            
            # Stat card
            dwg.add(dwg.rect(
                insert=(x, y),
                size=(card_width, card_height),
                class_='stat-card'
            ))
            
            # Stat value (bright and prominent)
            dwg.add(dwg.text(
                value,
                insert=(x + card_width/2, y + 55),
                text_anchor='middle',
                class_='stat-value'
            ))
            
            # Stat label
            dwg.add(dwg.text(
                label,
                insert=(x + card_width/2, y + 80),
                text_anchor='middle',
                class_='stat-label'
            ))
            
            # Stat sublabel
            dwg.add(dwg.text(
                sublabel,
                insert=(x + card_width/2, y + 100),
                text_anchor='middle',
                class_='stat-sublabel'
            ))
        
        # Cultivation progress bar
        progress_y = 450
        progress_width = 900
        progress_height = 30
        progress_x = 90
        
        # Progress text above bar
        progress_percent = (stats['immortal_level'] / 99) * 100
        dwg.add(dwg.text(
            f"Cultivation Progress to Ascension",
            insert=(progress_x + progress_width/2, progress_y - 15),
            text_anchor='middle',
            class_='progress-text'
        ))
        
        dwg.add(dwg.rect(
            insert=(progress_x, progress_y),
            size=(progress_width, progress_height),
            class_='progress-bg'
        ))
        
        # Progress fill
        fill_width = (stats['immortal_level'] / 99) * progress_width
        dwg.add(dwg.rect(
            insert=(progress_x, progress_y),
            size=(fill_width, progress_height),
            class_='progress-fill'
        ))
        
        # Progress percentage text
        dwg.add(dwg.text(
            f"{stats['immortal_level']}/99 ({progress_percent:.1f}%)",
            insert=(progress_x + progress_width/2, progress_y + progress_height + 25),
            text_anchor='middle',
            class_='stat-label'
        ))
        
        dwg.save()
        print("✅ Cultivation stats visualization generated!")

    def generate_all_visualizations(self):
        """Generate all visualizations"""
        self.create_skill_bars_svg()
        self.create_elemental_affinities_svg()
        self.create_cultivation_stats_svg()
        print("🎉 All visualizations completed with divine clarity!")

def main():
    print("=" * 60)
    print("   🌟 Divine Cultivation Visualization Generator 🌟")
    print("=" * 60 + "\n")
    
    try:
        generator = SVGGenerator()
        generator.generate_all_visualizations()
        
        print("\n" + "=" * 60)
        print("   ✨ Success! The heavens smile upon your visualizations")
        print("=" * 60)
        
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())