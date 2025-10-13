#!/usr/bin/env python3
"""
⚔️ RPG Skill Level Calculator
Transforms GitHub data into RPG-style skill levels
"""

import os
import json
import math
from datetime import datetime

class SkillGrimoire:
    def __init__(self):
        self.data_dir = 'data'
        
        # Load GitHub data
        with open(f'{self.data_dir}/github_data.json', 'r') as f:
            self.github_data = json.load(f)
        
        # RPG level calculation parameters
        self.BASE_XP = 100
        self.XP_MULTIPLIER = 1.5
        
    def bytes_to_xp(self, bytes_count):
        """Convert code bytes to experience points"""
        # Each 1000 bytes = 1 XP
        return bytes_count / 1000
    
    def calculate_level(self, xp):
        """Calculate RPG level from XP (exponential curve)"""
        if xp <= 0:
            return 1
        
        # Level = floor(log(XP/BASE_XP) / log(XP_MULTIPLIER)) + 1
        level = math.floor(math.log(xp / self.BASE_XP) / math.log(self.XP_MULTIPLIER)) + 1
        return max(1, min(level, 99))  # Cap at level 99
    
    def xp_for_next_level(self, current_level):
        """Calculate XP needed for next level"""
        return self.BASE_XP * (self.XP_MULTIPLIER ** current_level)
    
    def get_skill_rank(self, level):
        """Get rank title based on level"""
        if level >= 90: return "⚡ Dark Sovereign"
        if level >= 80: return "🔥 Archmage"
        if level >= 70: return "💀 Necromancer Lord"
        if level >= 60: return "🗡️ Shadow Master"
        if level >= 50: return "⚔️ Battle Mage"
        if level >= 40: return "🛡️ Dark Knight"
        if level >= 30: return "🌙 Shadow Warrior"
        if level >= 20: return "⚰️ Apprentice Warlock"
        if level >= 10: return "🦇 Initiate"
        return "🕯️ Novice"
    
    def calculate_language_skills(self):
        """Calculate skill levels for all languages"""
        print("⚔️ Calculating dark skill levels...\n")
        
        lang_bytes = self.github_data['languages']['by_bytes']
        lang_repos = self.github_data['languages']['by_repos']
        
        skills = {}
        total_bytes = sum(lang_bytes.values())
        
        for lang, bytes_count in sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True):
            xp = self.bytes_to_xp(bytes_count)
            level = self.calculate_level(xp)
            percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
            
            skills[lang] = {
                "xp": int(xp),
                "level": level,
                "next_level_xp": int(self.xp_for_next_level(level)),
                "percentage": round(percentage, 1),
                "repo_count": lang_repos.get(lang, 0),
                "rank": self.get_skill_rank(level),
                "progress_bar": self.generate_progress_bar(level)
            }
            
            print(f"  {lang:15} | Level {level:2} | {skills[lang]['rank']}")
        
        return skills
    
    def generate_progress_bar(self, level, max_level=99):
        """Generate visual progress bar"""
        bars = int((level / max_level) * 10)
        return '█' * bars + '░' * (10 - bars)
    
    def calculate_overall_stats(self, skills):
        """Calculate overall player statistics"""
        total_xp = sum(s['xp'] for s in skills.values())
        avg_level = sum(s['level'] for s in skills.values()) / len(skills) if skills else 1
        max_level = max((s['level'] for s in skills.values()), default=1)
        
        overall_level = self.calculate_level(total_xp)
        
        return {
            "total_xp": int(total_xp),
            "overall_level": overall_level,
            "average_skill_level": round(avg_level, 1),
            "highest_skill_level": max_level,
            "total_skills": len(skills),
            "rank": self.get_skill_rank(overall_level),
            "progress_bar": self.generate_progress_bar(overall_level)
        }
    
    def categorize_skills(self, skills):
        """Categorize skills by type"""
        
        categories = {
            "combat": {  # Programming languages
                "title": "⚔️ Combat Skills (Languages)",
                "skills": {}
            },
            "magic": {  # Frameworks
                "title": "🔮 Magic Arts (Frameworks)",
                "skills": {}
            },
            "defense": {  # DevOps/Infrastructure
                "title": "🛡️ Defensive Arts (Infrastructure)",
                "skills": {}
            }
        }
        
        # Language categorization
        combat_langs = ['Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 
                       'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Dart']
        magic_langs = ['Vue', 'React', 'Angular', 'Svelte', 'Next.js', 'HTML', 'CSS']
        defense_langs = ['Shell', 'Dockerfile', 'HCL', 'Makefile', 'YAML']
        
        for lang, data in skills.items():
            if lang in combat_langs:
                categories['combat']['skills'][lang] = data
            elif lang in magic_langs:
                categories['magic']['skills'][lang] = data
            elif lang in defense_langs:
                categories['defense']['skills'][lang] = data
            else:
                categories['combat']['skills'][lang] = data  # Default to combat
        
        return categories
    
    def save_skill_data(self):
        """Save calculated skill data"""
        print("🎮 Generating RPG skill grimoire...\n")
        
        skills = self.calculate_language_skills()
        overall = self.calculate_overall_stats(skills)
        categories = self.categorize_skills(skills)
        
        streak_data = self.github_data['streaks']
        
        rpg_data = {
            "last_updated": datetime.now().isoformat(),
            "player": {
                "name": self.github_data['username'],
                "level": overall['overall_level'],
                "rank": overall['rank'],
                "total_xp": overall['total_xp'],
                "progress_bar": overall['progress_bar']
            },
            "overall_stats": overall,
            "skills": skills,
            "categories": categories,
            "achievements": {
                "current_streak": streak_data['current'],
                "longest_streak": streak_data['longest'],
                "total_contributions": self.github_data['total_contributions'],
                "followers": self.github_data['followers'],
                "repositories": self.github_data['repositories']['own']
            },
            "metadata": {
                "total_languages": len(skills),
                "darkest_coding_hour": self.github_data['patterns']['darkest_hour']
            }
        }
        
        output_file = f'{self.data_dir}/skills.json'
        with open(output_file, 'w') as f:
            json.dump(rpg_data, f, indent=2)
        
        print(f"\n✅ Skill grimoire saved to {output_file}")
        print(f"   🎯 Overall Level: {overall['overall_level']}")
        print(f"   ⭐ Rank: {overall['rank']}")
        print(f"   📊 Total Skills: {len(skills)}")
        
        return rpg_data

def main():
    print("🎮" * 30)
    print("   RPG SKILL CALCULATION RITUAL")
    print("🎮" * 30 + "\n")
    
    try:
        grimoire = SkillGrimoire()
        data = grimoire.save_skill_data()
        
        print("\n" + "⚔️" * 30)
        print("   CHARACTER SHEET UPDATED")
        print("⚔️" * 30)
        
        return 0
    except Exception as e:
        print(f"\n💀 RITUAL FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())