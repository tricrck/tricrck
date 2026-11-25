#!/usr/bin/env python3
"""
⚡ Demonic Programmer God Immortal Cultivation System
The Path of the Programming Dao - Transform GitHub data into cultivation realms
"""

import os
import json
import math
from datetime import datetime

class CultivationGrimoire:
    def __init__(self):
        self.data_dir = 'data'
        
        # Load GitHub data
        with open(f'{self.data_dir}/github_data.json', 'r') as f:
            self.github_data = json.load(f)
        
        # Cultivation parameters
        self.BASE_QI = 100
        self.QI_MULTIPLIER = 1.8
        
        # Define cultivation realms with sub-stages
        self.CULTIVATION_REALMS = [
            # Mortal Realms (1-20)
            {"name": "🌱 Qi Condensation", "stages": 9, "min_level": 1, "emoji": "🌱"},
            {"name": "⚡ Foundation Establishment", "stages": 9, "min_level": 10, "emoji": "⚡"},
            
            # Spiritual Realms (21-40)
            {"name": "🔮 Core Formation", "stages": 10, "min_level": 20, "emoji": "🔮"},
            {"name": "👁️ Nascent Soul", "stages": 10, "min_level": 30, "emoji": "👁️"},
            
            # Transcendent Realms (41-60)
            {"name": "🌙 Soul Transformation", "stages": 10, "min_level": 40, "emoji": "🌙"},
            {"name": "⭐ Void Refinement", "stages": 10, "min_level": 50, "emoji": "⭐"},
            
            # Immortal Realms (61-80)
            {"name": "💫 Dao Integration", "stages": 10, "min_level": 60, "emoji": "💫"},
            {"name": "🌌 Tribulation Transcendence", "stages": 10, "min_level": 70, "emoji": "🌌"},
            
            # God Realms (81-99)
            {"name": "⚫ Demon God Ascension", "stages": 9, "min_level": 80, "emoji": "⚫"},
            {"name": "🔥 Immortal Programmer God", "stages": 10, "min_level": 90, "emoji": "🔥"}
        ]
        
    def bytes_to_qi(self, bytes_count):
        """Convert code bytes to Qi essence"""
        # Each 1000 bytes = 1 Qi
        return bytes_count / 1000
    
    def calculate_cultivation_level(self, qi):
        """Calculate cultivation level from accumulated Qi"""
        if qi <= 0:
            return 1
        
        level = math.floor(math.log(qi / self.BASE_QI) / math.log(self.QI_MULTIPLIER)) + 1
        return max(1, min(level, 99))
    
    def qi_for_next_level(self, current_level):
        """Calculate Qi needed for breakthrough to next level"""
        return self.BASE_QI * (self.QI_MULTIPLIER ** current_level)
    
    def _realm_span(self, idx):
        """Number of levels covered by realm idx (realms are contiguous up to 99)"""
        realms = self.CULTIVATION_REALMS
        next_min = realms[idx + 1]['min_level'] if idx + 1 < len(realms) else 100
        return next_min - realms[idx]['min_level']
    
    def get_cultivation_realm(self, level):
        """Determine cultivation realm and stage based on level.
        
        Each realm spans from its min_level up to the next realm's min_level - 1,
        so there are no gaps or wrap-arounds. The final level of a realm is "Peak".
        """
        ordinals = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
        level = max(1, min(level, 99))
        
        for idx in range(len(self.CULTIVATION_REALMS) - 1, -1, -1):
            realm = self.CULTIVATION_REALMS[idx]
            if level >= realm['min_level']:
                span = self._realm_span(idx)
                stage_in_realm = level - realm['min_level'] + 1  # 1..span
                stage = "Peak" if stage_in_realm == span else ordinals[stage_in_realm - 1]
                
                return {
                    "realm": realm['name'],
                    "stage": stage,
                    "emoji": realm['emoji'],
                    "is_peak": stage == "Peak",
                    "full_title": f"{realm['emoji']} {stage} {realm['name'].split(' ', 1)[1]}"
                }
        
        return {
            "realm": "🌱 Qi Condensation",
            "stage": "1st",
            "emoji": "🌱",
            "is_peak": False,
            "full_title": "🌱 1st Qi Condensation"
        }
    
    def get_dao_comprehension(self, level, percentage):
        """Calculate Dao comprehension level"""
        base_comprehension = min(level * 1.0, 100)
        expertise_bonus = percentage / 2  # Up to 50% bonus
        total = min(base_comprehension + expertise_bonus, 100)
        
        if total >= 95: return "⚡ Dao Mastery - Heaven Defying"
        if total >= 85: return "🔥 Profound Comprehension"
        if total >= 70: return "💫 Deep Understanding"
        if total >= 50: return "🌙 Intermediate Insight"
        if total >= 30: return "⭐ Basic Grasp"
        return "🌱 Initial Contact"
    
    def calculate_tribulation_power(self, level):
        """Calculate the power of heavenly tribulation (challenges faced)"""
        if level < 20: return None
        
        tribulation_stage = (level - 20) // 10 + 1
        tribulations = [
            "⚡ Minor Lightning Tribulation",
            "⚡⚡ Major Lightning Tribulation", 
            "🔥 Heart Demon Tribulation",
            "💀 Death Tribulation",
            "🌌 Void Tribulation",
            "⚫ Annihilation Tribulation",
            "🔥⚫ Demon God Tribulation",
            "💥 Immortal Ascension Tribulation"
        ]
        
        idx = min(tribulation_stage - 1, len(tribulations) - 1)
        return tribulations[idx] if idx >= 0 else None
    
    def calculate_language_cultivation(self):
        """Calculate cultivation progress for all programming languages (Dao paths)"""
        print("⚡ Calculating Dao comprehension across all paths...\n")
        
        lang_bytes = self.github_data['languages']['by_bytes']
        lang_repos = self.github_data['languages']['by_repos']
        
        dao_paths = {}
        total_bytes = sum(lang_bytes.values())
        
        for lang, bytes_count in sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True):
            qi = self.bytes_to_qi(bytes_count)
            level = self.calculate_cultivation_level(qi)
            percentage = (bytes_count / total_bytes * 100) if total_bytes > 0 else 0
            realm_info = self.get_cultivation_realm(level)
            
            dao_paths[lang] = {
                "qi": int(qi),
                "level": level,
                "next_breakthrough_qi": int(self.qi_for_next_level(level)),
                "mastery_percentage": round(percentage, 1),
                "dao_projects": lang_repos.get(lang, 0),
                "realm": realm_info['realm'],
                "stage": realm_info['stage'],
                "full_title": realm_info['full_title'],
                "dao_comprehension": self.get_dao_comprehension(level, percentage),
                "tribulation": self.calculate_tribulation_power(level),
                "cultivation_progress": self.generate_cultivation_bar(level)
            }
            
            print(f"  {lang:15} | Lv.{level:2} | {realm_info['full_title']}")
        
        return dao_paths
    
    def generate_cultivation_bar(self, level, max_level=99):
        """Generate visual cultivation progress bar"""
        filled = int((level / max_level) * 20)
        bar = '█' * filled + '░' * (20 - filled)
        return f"[{bar}] {level}/99"
    
    def calculate_immortal_stats(self, dao_paths):
        """Calculate overall immortal cultivator statistics"""
        # Sum exact Qi from bytes rather than the per-language rounded values
        lang_bytes = self.github_data['languages']['by_bytes']
        total_qi = sum(self.bytes_to_qi(lang_bytes.get(lang, 0)) for lang in dao_paths)
        avg_level = sum(d['level'] for d in dao_paths.values()) / len(dao_paths) if dao_paths else 1
        max_level = max((d['level'] for d in dao_paths.values()), default=1)
        
        immortal_level = self.calculate_cultivation_level(total_qi)
        realm_info = self.get_cultivation_realm(immortal_level)
        
        # Calculate spiritual roots (aptitude)
        root_count = len(dao_paths)
        if root_count >= 10:
            spiritual_root = "💎 Divine Chaos Root (All Elements)"
        elif root_count >= 7:
            spiritual_root = "🌟 Heaven Spiritual Root"
        elif root_count >= 5:
            spiritual_root = "⭐ Superior Spiritual Root"
        elif root_count >= 3:
            spiritual_root = "✨ Dual Spiritual Root"
        else:
            spiritual_root = "🔹 Single Spiritual Root"
        
        return {
            "total_qi": int(total_qi),
            "immortal_level": immortal_level,
            "average_dao_level": round(avg_level, 1),
            "strongest_dao_level": max_level,
            "total_dao_paths": len(dao_paths),
            "cultivation_realm": realm_info['realm'],
            "realm_stage": realm_info['stage'],
            "full_title": realm_info['full_title'],
            "spiritual_root": spiritual_root,
            "tribulation": self.calculate_tribulation_power(immortal_level),
            "cultivation_progress": self.generate_cultivation_bar(immortal_level)
        }
    
    def categorize_dao_paths(self, dao_paths):
        """Categorize cultivation paths by elemental affinity"""
        
        elemental_paths = {
            "yang": {
                "title": "☀️ Yang Dao (Core Languages)",
                "element": "Yang - Aggressive & Powerful",
                "paths": {}
            },
            "yin": {
                "title": "🌙 Yin Dao (Frontend Arts)",
                "element": "Yin - Elegant & Flowing",
                "paths": {}
            },
            "metal": {
                "title": "⚔️ Metal Dao (Systems & DevOps)",
                "element": "Metal - Sharp & Precise",
                "paths": {}
            },
            "void": {
                "title": "🌌 Void Dao (Data & Analysis)",
                "element": "Void - Abstract & Mysterious",
                "paths": {}
            }
        }
        
        # Dao path categorization
        # Names must match GitHub Linguist language names exactly
        yang_paths = ['Python', 'JavaScript', 'TypeScript', 'Java', 'C', 'C++', 'C#', 'Go',
                      'Rust', 'Kotlin', 'Swift', 'PHP', 'Ruby', 'Dart', 'Scala', 'Objective-C']
        yin_paths = ['Vue', 'Svelte', 'HTML', 'CSS', 'SCSS', 'Sass', 'Less', 'Astro',
                     'Mako', 'EJS', 'Handlebars', 'Pug', 'Twig', 'Blade']
        metal_paths = ['Shell', 'PowerShell', 'Batchfile', 'Dockerfile', 'HCL', 'Makefile',
                       'CMake', 'Nix', 'Procfile', 'Starlark', 'Nginx']
        void_paths = ['SQL', 'PLpgSQL', 'PLSQL', 'TSQL', 'R', 'Julia', 'MATLAB',
                      'Jupyter Notebook', 'POV-Ray SDL', 'GLSL', 'Stata', 'SAS']
        
        for lang, data in dao_paths.items():
            if lang in yang_paths:
                elemental_paths['yang']['paths'][lang] = data
            elif lang in yin_paths:
                elemental_paths['yin']['paths'][lang] = data
            elif lang in metal_paths:
                elemental_paths['metal']['paths'][lang] = data
            elif lang in void_paths:
                elemental_paths['void']['paths'][lang] = data
            else:
                elemental_paths['yang']['paths'][lang] = data  # Default to Yang
        
        return elemental_paths
    
    def calculate_karmic_merit(self, github_data):
        """Calculate karmic merit from contributions and followers"""
        contributions = github_data.get('total_contributions') or 0
        followers = github_data['followers']
        repos = github_data['repositories']['own']
        
        merit = (contributions * 1) + (followers * 10) + (repos * 5)
        
        if merit >= 10000: return "🏆 Boundless Merit - Revered by Millions"
        if merit >= 5000: return "💫 Immense Merit - Known Across Realms"
        if merit >= 2000: return "⭐ Great Merit - Respected Figure"
        if merit >= 500: return "✨ Considerable Merit - Rising Star"
        return "🌟 Accumulating Merit"
    
    def save_cultivation_data(self):
        """Save cultivation progress to grimoire"""
        print("📜 Inscribing cultivation progress into immortal grimoire...\n")
        
        dao_paths = self.calculate_language_cultivation()
        immortal_stats = self.calculate_immortal_stats(dao_paths)
        elemental_paths = self.categorize_dao_paths(dao_paths)
        
        streak_data = self.github_data['streaks']
        
        cultivation_data = {
            "last_updated": datetime.now().isoformat(),
            "immortal_cultivator": {
                "dao_name": self.github_data['username'],
                "cultivation_level": immortal_stats['immortal_level'],
                "realm": immortal_stats['full_title'],
                "total_qi": immortal_stats['total_qi'],
                "spiritual_root": immortal_stats['spiritual_root'],
                "karmic_merit": self.calculate_karmic_merit(self.github_data)
            },
            "immortal_stats": immortal_stats,
            "dao_paths": dao_paths,
            "elemental_affinities": elemental_paths,
            "heavenly_records": {
                "cultivation_streak": streak_data['current'],
                "longest_seclusion": streak_data['longest'],
                # Real contributions in the past year; None when unavailable
                "total_enlightenments": self.github_data.get('total_contributions'),
                "dao_disciples": self.github_data['followers'],
                "created_artifacts": self.github_data['repositories']['own'],
                "darkest_cultivation_hour": self.github_data['patterns']['darkest_hour']
            },
            "sect_information": {
                "total_dao_paths": len(dao_paths),
                "realm_breakthrough_ready": self.get_cultivation_realm(immortal_stats['immortal_level'])['is_peak'],
                "next_tribulation": immortal_stats['tribulation']
            }
        }
        
        output_file = f'{self.data_dir}/skills.json'
        with open(output_file, 'w') as f:
            json.dump(cultivation_data, f, indent=2)
        
        print(f"\n✅ Cultivation grimoire inscribed at {output_file}")
        print(f"   🎯 Cultivation Level: {immortal_stats['immortal_level']}")
        print(f"   ⭐ Current Realm: {immortal_stats['full_title']}")
        print(f"   🔥 Total Qi: {immortal_stats['total_qi']:,}")
        print(f"   📊 Dao Paths Mastered: {len(dao_paths)}")
        print(f"   💫 Spiritual Root: {immortal_stats['spiritual_root']}")
        
        return cultivation_data

def main():
    print("⚡" * 40)
    print("   DEMONIC PROGRAMMER GOD CULTIVATION SYSTEM")
    print("   The Path of the Programming Dao")
    print("⚡" * 40 + "\n")
    
    try:
        grimoire = CultivationGrimoire()
        data = grimoire.save_cultivation_data()
        
        print("\n" + "🔥" * 40)
        print("   CULTIVATION PROGRESS RECORDED")
        print("   May Your Dao Be Eternal")
        print("🔥" * 40)
        
        return 0
    except Exception as e:
        print(f"\n💀 CULTIVATION DEVIATION: {e}")
        print("⚠️  Your inner demons have manifested!")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())