"""
最下層ループエッジあり: 分岐数2のシミュレーション
"""
import sys
sys.path.append('../..')
from research_simulation import OrganizationGraph, ResearchSimulator

if __name__ == "__main__":
    print("=== 最下層ループエッジあり: 分岐数2のシミュレーション ===\n")

    # 7階層、分岐数2、最下層にループエッジ
    print("組織構造: 7階層（CEO, CTO, Director, Manager, TeamLead, Senior, Junior）")
    print("分岐数: 2")
    print("特殊構造: 最下層（Junior）にリング状のループエッジを追加")
    org = OrganizationGraph(branches=2, height=6, structure_type="baseline_with_loop")
    print(f"ノード数: {len(org.G.nodes())}")
    print(f"エッジ数: {len(org.G.edges())}")

    # 最下層のエッジ数を確認
    depths = {node: org.get_depth(node) for node in org.G.nodes()}
    max_depth = max(depths.values())
    bottom_nodes = [n for n, d in depths.items() if d == max_depth]
    print(f"最下層ノード数: {len(bottom_nodes)}")
    print(f"追加ループエッジ数: {len(bottom_nodes)}\n")

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
