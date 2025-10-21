import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from collections import defaultdict
import copy

# pydotの有無をチェック
try:
    import pydot
    from networkx.drawing.nx_pydot import graphviz_layout
    LAYOUT_ENGINE = "graphviz"
except ImportError:
    LAYOUT_ENGINE = "spring"


class MovingAgent:
    """グラフ上を移動するエージェントクラス"""
    def __init__(self, agent_id, start_node, move_count, movement_rule="hierarchy"):
        self.agent_id = agent_id
        self.current_position = start_node
        self.start_node = start_node
        self.remaining_moves = move_count
        self.total_moves = move_count
        self.movement_rule = movement_rule
        self.path_history = [start_node]  # 移動履歴

    def is_active(self):
        """まだ移動可能か"""
        return self.remaining_moves > 0

    def move_to(self, next_node):
        """指定ノードへ移動"""
        self.current_position = next_node
        self.remaining_moves -= 1
        self.path_history.append(next_node)


class OrganizationGraph:
    """組織構造グラフクラス"""
    def __init__(self, branches=2, height=3, structure_type="baseline"):
        self.structure_type = structure_type
        self.G = None
        self.role_mapping = {}
        self.depth_mapping = {}
        self.visit_count = defaultdict(int)  # ノード訪問回数
        self.pos = None

        self._create_structure(branches, height)
        self._calculate_layout()

    def _create_structure(self, branches, height):
        """組織構造を生成"""
        if self.structure_type == "baseline":
            self._create_baseline(branches, height)
        elif self.structure_type == "baseline_with_loop":
            self._create_baseline_with_loop(branches, height)
        elif self.structure_type == "dual_middle":
            self._create_dual_middle_management(branches, height)
        elif self.structure_type == "small_teams":
            self._create_small_teams(height)
        elif self.structure_type == "large_teams":
            self._create_large_teams(height)
        elif self.structure_type == "downsizing_30":
            self._create_downsized(branches, height, 0.3)
        elif self.structure_type == "downsizing_50":
            self._create_downsized(branches, height, 0.5)

    def _create_baseline(self, branches, height):
        """ベースライン: シンプルな階層構造"""
        self.G = nx.balanced_tree(branches, height)
        self._assign_roles_and_depths()

    def _create_baseline_with_loop(self, branches, height):
        """ベースライン + 最下層にループエッジを追加"""
        self.G = nx.balanced_tree(branches, height)

        # 最下層のノードを特定
        depths = nx.single_source_shortest_path_length(self.G, 0)
        max_depth = max(depths.values())
        bottom_layer_nodes = [node for node, depth in depths.items() if depth == max_depth]

        # 最下層のノード間にループエッジを追加（リング状に接続）
        for i in range(len(bottom_layer_nodes)):
            node1 = bottom_layer_nodes[i]
            node2 = bottom_layer_nodes[(i + 1) % len(bottom_layer_nodes)]
            self.G.add_edge(node1, node2)

        self._assign_roles_and_depths()

    def _create_dual_middle_management(self, branches, height):
        """中間管理職を2人配置した構造"""
        self.G = nx.balanced_tree(branches, height)

        # 中間管理職層（depth=2）のノードを特定
        depths = nx.single_source_shortest_path_length(self.G, 0)
        middle_nodes = [node for node, depth in depths.items() if depth == 2]

        # 各中間管理職ノードを複製（仮想的に2人配置）
        self.dual_middle_pairs = {}
        node_offset = len(self.G.nodes())

        for middle_node in middle_nodes:
            duplicate_node = node_offset
            self.G.add_node(duplicate_node)

            # 元のノードと同じ接続を持つ
            parent = list(self.G.predecessors(middle_node))[0] if list(self.G.predecessors(middle_node)) else None
            if parent is not None:
                self.G.add_edge(parent, duplicate_node)

            # 子ノードへの接続も共有
            children = list(self.G.successors(middle_node))
            for child in children:
                self.G.add_edge(duplicate_node, child)

            self.dual_middle_pairs[middle_node] = duplicate_node
            node_offset += 1

        self._assign_roles_and_depths()

    def _create_small_teams(self, height):
        """極小チーム（各チーム2-3名）"""
        self.G = nx.balanced_tree(2, height)
        self._assign_roles_and_depths()

    def _create_large_teams(self, height):
        """大規模チーム（各チーム8-10名）"""
        self.G = nx.balanced_tree(8, height)
        self._assign_roles_and_depths()

    def _create_downsized(self, branches, height, downsize_ratio):
        """人員削減版（ノードを削減）"""
        self.G = nx.balanced_tree(branches, height)

        # 末端ノード以外からランダムに削減
        all_nodes = list(self.G.nodes())
        leaf_nodes = [n for n in all_nodes if self.G.out_degree(n) == 0]
        non_leaf_nodes = [n for n in all_nodes if n not in leaf_nodes and n != 0]

        # 削減対象ノードを選択
        num_to_remove = int(len(non_leaf_nodes) * downsize_ratio)
        nodes_to_remove = random.sample(non_leaf_nodes, num_to_remove)

        self.G.remove_nodes_from(nodes_to_remove)
        self._assign_roles_and_depths()

    def _assign_roles_and_depths(self):
        """役職と階層深さを割り当て"""
        if 0 not in self.G.nodes():
            # グラフが空または不正な場合
            return

        depths = nx.single_source_shortest_path_length(self.G, 0)

        for node in self.G.nodes():
            depth = depths.get(node, 0)
            self.depth_mapping[node] = depth

            if depth == 0:
                self.role_mapping[node] = "CEO"
            elif depth == 1:
                self.role_mapping[node] = "CTO"
            elif depth == 2:
                self.role_mapping[node] = "Director"
            elif depth == 3:
                self.role_mapping[node] = "Manager"
            elif depth == 4:
                self.role_mapping[node] = "TeamLead"
            elif depth == 5:
                self.role_mapping[node] = "Senior"
            elif depth == 6:
                self.role_mapping[node] = "Junior"
            else:
                self.role_mapping[node] = "Staff"

    def _calculate_layout(self):
        """レイアウトを計算"""
        if len(self.G.nodes()) == 0:
            self.pos = {}
            return

        # 大規模グラフの場合はレイアウト計算をスキップ
        if len(self.G.nodes()) > 1000:
            self.pos = {}
            return

        if LAYOUT_ENGINE == "graphviz":
            try:
                self.pos = graphviz_layout(self.G, prog='dot', root=0)
            except:
                try:
                    self.pos = nx.spring_layout(self.G)
                except:
                    self.pos = {}
        else:
            try:
                self.pos = nx.spring_layout(self.G)
            except:
                self.pos = {}

    def record_visit(self, node):
        """ノード訪問を記録"""
        self.visit_count[node] += 1

    def get_neighbors(self, node):
        """隣接ノードを取得"""
        if node not in self.G:
            return []
        return list(self.G.neighbors(node))

    def get_depth(self, node):
        """ノードの階層深さを取得"""
        return self.depth_mapping.get(node, 0)

    def get_role(self, node):
        """ノードの役職を取得"""
        return self.role_mapping.get(node, "Unknown")

    def calculate_centrality(self):
        """中心性指標を計算"""
        if len(self.G.nodes()) == 0:
            return {}

        centrality = {
            'betweenness': nx.betweenness_centrality(self.G),
            'closeness': nx.closeness_centrality(self.G),
            'degree': nx.degree_centrality(self.G),
        }

        # 固有ベクトル中心性は連結グラフでないと計算できない
        try:
            centrality['eigenvector'] = nx.eigenvector_centrality(self.G, max_iter=1000)
        except:
            centrality['eigenvector'] = {node: 0.0 for node in self.G.nodes()}

        return centrality


class MovementRuleEngine:
    """エージェント移動ルールエンジン"""

    @staticmethod
    def select_next_node(agent, org_graph, rule_type="hierarchy", selection_strategy="random"):
        """
        次の移動先ノードを選択

        rule_type: "hierarchy", "authority", "load_aware"
        selection_strategy: 中間管理職複数配置時の選択戦略（"random", "biased_70", "load_balanced"）
        """
        current_node = agent.current_position
        neighbors = org_graph.get_neighbors(current_node)

        if not neighbors:
            return None

        if rule_type == "hierarchy":
            return MovementRuleEngine._hierarchy_rule(agent, org_graph, neighbors)
        elif rule_type == "authority":
            return MovementRuleEngine._authority_rule(agent, org_graph, neighbors)
        elif rule_type == "load_aware":
            return MovementRuleEngine._load_aware_rule(agent, org_graph, neighbors)
        else:
            return random.choice(neighbors)

    @staticmethod
    def _hierarchy_rule(agent, org_graph, neighbors):
        """階層依存ルール"""
        current_depth = org_graph.get_depth(agent.current_position)

        # 隣接ノードを階層別に分類
        upward = [n for n in neighbors if org_graph.get_depth(n) < current_depth]
        same_level = [n for n in neighbors if org_graph.get_depth(n) == current_depth]
        downward = [n for n in neighbors if org_graph.get_depth(n) > current_depth]

        # 確率的に選択
        rand = random.random()

        if rand < 0.2 and upward:  # 20%で上位
            return random.choice(upward)
        elif rand < 0.5 and same_level:  # 30%で同階層
            return random.choice(same_level)
        elif downward:  # 50%で下位
            return random.choice(downward)

        return random.choice(neighbors)

    @staticmethod
    def _authority_rule(agent, org_graph, neighbors):
        """権限制約ルール"""
        current_depth = org_graph.get_depth(agent.current_position)

        upward = [n for n in neighbors if org_graph.get_depth(n) < current_depth]
        same_level = [n for n in neighbors if org_graph.get_depth(n) == current_depth]
        downward = [n for n in neighbors if org_graph.get_depth(n) > current_depth]

        rand = random.random()

        if rand < 0.70 and downward:  # 70%で下位
            return random.choice(downward)
        elif rand < 0.90 and same_level:  # 20%で同階層
            return random.choice(same_level)
        elif upward:  # 10%で上位
            return random.choice(upward)

        return random.choice(neighbors)

    @staticmethod
    def _load_aware_rule(agent, org_graph, neighbors):
        """負荷回避ルール"""
        rand = random.random()

        if rand < 0.60:  # 60%で低負荷ノード優先
            # 訪問回数が少ないノードを選択
            visit_counts = [(n, org_graph.visit_count[n]) for n in neighbors]
            min_visit = min(visit_counts, key=lambda x: x[1])
            candidates = [n for n, v in visit_counts if v == min_visit[1]]
            return random.choice(candidates)
        else:  # 40%で通常移動
            return random.choice(neighbors)


class ResearchSimulator:
    """研究用シミュレータ"""

    def __init__(self, org_graph, movement_rule="hierarchy", selection_strategy="random"):
        self.org_graph = org_graph
        self.movement_rule = movement_rule
        self.selection_strategy = selection_strategy
        self.agents = []
        self.simulation_history = []

    def generate_agent_move_count(self):
        """エージェント移動回数を確率分布に従って生成"""
        rand = random.random()
        if rand < 0.55:
            return 10
        elif rand < 0.85:  # 0.55 + 0.30
            return 20
        elif rand < 0.95:  # 0.85 + 0.10
            return 40
        else:
            return 80

    def create_agent(self, agent_id=None):
        """エージェントを生成"""
        if agent_id is None:
            agent_id = f"Agent_{len(self.agents)}"

        # ランダムな開始ノード
        start_node = random.choice(list(self.org_graph.G.nodes()))
        move_count = self.generate_agent_move_count()

        agent = MovingAgent(agent_id, start_node, move_count, self.movement_rule)
        self.agents.append(agent)

        # 開始ノードの訪問を記録
        self.org_graph.record_visit(start_node)

        return agent

    def run_single_simulation(self, num_agents=100):
        """単一シミュレーション実行"""
        # エージェント生成
        self.agents = []
        for i in range(num_agents):
            self.create_agent(f"Agent_{i}")

        # 全エージェントが移動完了するまで
        while any(agent.is_active() for agent in self.agents):
            for agent in self.agents:
                if agent.is_active():
                    next_node = MovementRuleEngine.select_next_node(
                        agent, self.org_graph, self.movement_rule, self.selection_strategy
                    )

                    if next_node is not None:
                        agent.move_to(next_node)
                        self.org_graph.record_visit(next_node)

    def run_multiple_simulations(self, num_simulations=1000, num_agents_per_sim=100):
        """複数回シミュレーション実行"""
        results = []

        for sim_id in range(num_simulations):
            # 訪問カウントをリセット
            self.org_graph.visit_count = defaultdict(int)

            # シミュレーション実行
            self.run_single_simulation(num_agents_per_sim)

            # 結果を記録
            results.append(copy.deepcopy(dict(self.org_graph.visit_count)))

            if (sim_id + 1) % 100 == 0:
                print(f"完了: {sim_id + 1}/{num_simulations} シミュレーション")

        return results

    def analyze_results(self, results):
        """結果分析"""
        # 各ノードの平均訪問回数を計算
        all_nodes = list(self.org_graph.G.nodes())
        avg_visits = {node: 0 for node in all_nodes}

        for result in results:
            for node in all_nodes:
                avg_visits[node] += result.get(node, 0)

        for node in all_nodes:
            avg_visits[node] /= len(results)

        # 役職別集計
        role_visits = defaultdict(list)
        for node, visits in avg_visits.items():
            role = self.org_graph.get_role(node)
            role_visits[role].append(visits)

        # 統計量計算
        role_stats = {}
        for role, visits_list in role_visits.items():
            role_stats[role] = {
                'mean': np.mean(visits_list),
                'std': np.std(visits_list),
                'max': np.max(visits_list),
                'min': np.min(visits_list)
            }

        return {
            'avg_visits': avg_visits,
            'role_stats': role_stats
        }


# メイン実行
if __name__ == "__main__":
    print("=== 中間管理職負荷測定シミュレーション ===\n")

    # 7階層組織構造
    print("組織構造: 7階層（CEO, CTO, Director, Manager, TeamLead, Senior, Junior）")
    org = OrganizationGraph(branches=2, height=6, structure_type="baseline")
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
    # 階層順に表示
    role_order = ["CEO", "CTO", "Director", "Manager", "TeamLead", "Senior", "Junior"]
    for role in role_order:
        if role in analysis['role_stats']:
            stats = analysis['role_stats'][role]
            print(f"\n{role} (depth={list(org.depth_mapping.values())[list(org.role_mapping.values()).index(role)]}):")
            print(f"  平均訪問回数: {stats['mean']:.2f}")
            print(f"  標準偏差: {stats['std']:.2f}")
            print(f"  最大: {stats['max']:.2f}")
            print(f"  最小: {stats['min']:.2f}")
