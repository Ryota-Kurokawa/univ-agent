"""
分岐数10のシミュレーション
1人の上長に対して10人の部下
"""
import sys
sys.path.append('.')
from research_simulation import OrganizationGraph, ResearchSimulator

if __name__ == "__main__":
    print("=== 分岐数10のシミュレーション ===\n")

    # 7階層、分岐数10
    print("組織構造: 7階層（CEO, CTO, Director, Manager, TeamLead, Senior, Junior）")
    print("分岐数: 10")
    org = OrganizationGraph(branches=10, height=6, structure_type="baseline")
    print(f"ノード数: {len(org.G.nodes())}")
    print(f"エッジ数: {len(org.G.edges())}\n")

    # シミュレーション実行
    print("ルール: 階層依存ルール")
    sim = ResearchSimulator(org, movement_rule="hierarchy")

    print("シミュレーション開始（1000回試行）...")
    results = sim.run_multiple_simulations(num_simulations=1000, num_agents_per_sim=100)

    print("\n=== 分析結果 ===")
    analysis = sim.analyze_results(results)

    print("\n役職別統計:")
    role_order = ["CEO", "CTO", "Director", "Manager", "TeamLead", "Senior", "Junior"]
    for role in role_order:
        if role in analysis['role_stats']:
            stats = analysis['role_stats'][role]
            print(f"\n{role}:")
            print(f"  平均訪問回数: {stats['mean']:.2f}")
            print(f"  標準偏差: {stats['std']:.2f}")
            print(f"  最大: {stats['max']:.2f}")
            print(f"  最小: {stats['min']:.2f}")
