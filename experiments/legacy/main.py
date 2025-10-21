import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import copy
from collections import defaultdict
import numpy as np

# pydotの有無をチェック
try:
    import pydot
    from networkx.drawing.nx_pydot import graphviz_layout
    LAYOUT_ENGINE = "graphviz"
    print("✓ pydotライブラリが見つかりました。階層レイアウトを使用します。")
except ImportError:
    LAYOUT_ENGINE = "spring"
    print("警告: 'pydot'またはGraphviz本体が見つかりません。代替のspring_layoutで描画します。")


class InformationPacket:
    """情報パケットクラス - ハイコンテクスト情報の伝達をモデル化"""
    def __init__(self, content, info_type="technical", context_level=1.0, urgency=1):
        self.content = content
        self.info_type = info_type  # "strategic", "technical", "operational"
        self.context_level = context_level  # 1.0 = フルコンテクスト, 0.0 = コンテクスト完全消失
        self.urgency = urgency  # 1-5: 緊急度
        self.path = []  # 伝達経路を記録
        self.original_context = context_level  # 元のコンテクストレベル
    
    def degrade_context(self, sender_role, receiver_role):
        """役割に応じてコンテクスト情報が劣化"""
        # 同じ役割間では劣化が少ない
        if sender_role == receiver_role:
            degradation = 0.05
        # 技術系同士
        elif sender_role in ["CTO", "TechLead", "Engineer"] and receiver_role in ["CTO", "TechLead", "Engineer"]:
            degradation = 0.1
        # 階層を跨ぐ場合
        elif (sender_role in ["CEO", "CTO"] and receiver_role in ["Engineer"]) or \
             (sender_role in ["Engineer"] and receiver_role in ["CEO", "CTO"]):
            degradation = 0.2
        else:
            degradation = 0.15
        
        self.context_level = max(0.0, self.context_level - degradation)
        return self


class Agent:
    """IT企業のエージェントクラス"""
    def __init__(self, agent_id, initial_node, role="Engineer", initial_info=None):
        self.agent_id = agent_id
        self.position = initial_node
        self.role = role
        self.information_inbox = []  # 受信した情報
        self.knowledge_base = set()  # 蓄積された知識
        self.communication_count = 0  # コミュニケーション回数
        
        # 役割に応じた特性
        self.context_ability = self._get_context_ability()
        self.authority_level = self._get_authority_level()
        
        if initial_info:
            self.knowledge_base.add(initial_info)
        
        print(f"エージェント {self.agent_id} ({self.role}) が生成されました。初期位置: {self.position}")

    def _get_context_ability(self):
        """役割に応じたコンテクスト理解能力"""
        context_abilities = {
            "CEO": 0.9,
            "CTO": 0.85,
            "TechLead": 0.8,
            "PM": 0.75,
            "Engineer": 0.7,
            "Designer": 0.65
        }
        return context_abilities.get(self.role, 0.6)
    
    def _get_authority_level(self):
        """役割に応じた権限レベル"""
        authority_levels = {
            "CEO": 5,
            "CTO": 4,
            "TechLead": 3,
            "PM": 3,
            "Engineer": 2,
            "Designer": 2
        }
        return authority_levels.get(self.role, 1)
    
    def send_information(self, info_packet, target_agent):
        """情報を他のエージェントに送信"""
        # コンテクスト劣化を適用
        info_packet.degrade_context(self.role, target_agent.role)
        info_packet.path.append((self.agent_id, target_agent.agent_id))
        
        target_agent.receive_information(info_packet)
        self.communication_count += 1
        target_agent.communication_count += 1
        
        return info_packet.context_level  # 伝達後のコンテクストレベルを返す
    
    def receive_information(self, info_packet):
        """情報を受信"""
        self.information_inbox.append(info_packet)
        # 理解度に応じて知識ベースに追加
        if info_packet.context_level >= (1.0 - self.context_ability):
            self.knowledge_base.add(info_packet.content)


class ITCompanyEnvironment:
    """IT企業環境クラス"""
    def __init__(self, branches=3, height=3):
        self.G = nx.balanced_tree(branches, height)
        self.agents = {}
        self.agent_counter = 0
        self.information_flow_log = []  # 情報伝達ログ
        
        # 階層構造とIT企業の役職をマッピング
        self.role_mapping = self._create_it_hierarchy()
        
        if LAYOUT_ENGINE == "graphviz":
            self.pos = graphviz_layout(self.G, prog='dot', root=0)
        else:
            self.pos = self._create_tree_layout()

        total_nodes = len(self.G.nodes)
        print(f"IT企業環境が生成されました (分岐数:{branches}, 高さ:{height}, 総ノード数:{total_nodes})。")
        print(f"役職マッピング: {self.role_mapping}")

    def _create_it_hierarchy(self):
        """IT企業の階層構造を作成"""
        depths = nx.single_source_shortest_path_length(self.G, 0)
        role_mapping = {}
        
        for node, depth in depths.items():
            if depth == 0:
                role_mapping[node] = "CEO"
            elif depth == 1:
                role_mapping[node] = "CTO"
            elif depth == 2:
                # 中間管理層
                role_mapping[node] = random.choice(["TechLead", "PM"])
            else:
                # 実務層
                role_mapping[node] = random.choice(["Engineer", "Engineer", "Designer"])  # エンジニア多め
        
        return role_mapping

    def add_agent(self, agent_id, start_node, role=None):
        """エージェントを追加"""
        if start_node not in self.G.nodes():
            return None
        
        # 役職が指定されていない場合は、ノードの役職を使用
        if role is None:
            role = self.role_mapping.get(start_node, "Engineer")
        
        agent = Agent(agent_id, start_node, role)
        self.agents[agent_id] = agent
        return agent

    def simulate_information_cascade(self, source_agent_id, info_content, info_type="technical"):
        """情報カスケードのシミュレーション"""
        if source_agent_id not in self.agents:
            return
        
        source_agent = self.agents[source_agent_id]
        info_packet = InformationPacket(info_content, info_type, context_level=1.0)
        
        print(f"\n=== 情報カスケード開始 ===")
        print(f"発信者: {source_agent_id} ({source_agent.role})")
        print(f"情報: {info_content}")
        
        # 同じノードの他のエージェントに情報を伝達
        agents_at_same_node = [a for a in self.agents.values() 
                              if a.position == source_agent.position and a.agent_id != source_agent_id]
        
        for target_agent in agents_at_same_node:
            remaining_context = source_agent.send_information(copy.deepcopy(info_packet), target_agent)
            self.information_flow_log.append({
                'from': source_agent_id,
                'to': target_agent.agent_id,
                'content': info_content,
                'context_remaining': remaining_context
            })
            print(f"  -> {target_agent.agent_id} ({target_agent.role}): コンテクスト残存 {remaining_context:.2f}")

    def analyze_network_centrality(self):
        """ネットワーク中心性を分析"""
        # エージェントの位置情報から実際のネットワークを構築
        actual_network = nx.Graph()
        for agent in self.agents.values():
            actual_network.add_node(agent.agent_id, 
                                  position=agent.position, 
                                  role=agent.role,
                                  communication_count=agent.communication_count)
        
        # エージェント間の接続を構築（同じノードまたは隣接ノードにいる場合）
        for agent1 in self.agents.values():
            for agent2 in self.agents.values():
                if agent1.agent_id != agent2.agent_id:
                    # 同じノードにいる場合、または隣接ノードにいる場合
                    if (agent1.position == agent2.position or 
                        agent2.position in self.G.neighbors(agent1.position)):
                        actual_network.add_edge(agent1.agent_id, agent2.agent_id)
        
        # 中心性指標を計算
        centrality_results = {}
        if len(actual_network.nodes()) > 0:
            centrality_results['betweenness'] = nx.betweenness_centrality(actual_network)
            centrality_results['closeness'] = nx.closeness_centrality(actual_network)
            centrality_results['degree'] = nx.degree_centrality(actual_network)
            centrality_results['eigenvector'] = nx.eigenvector_centrality(actual_network, max_iter=1000)
        
        return centrality_results, actual_network

    def print_centrality_analysis(self):
        """中心性分析結果を表示"""
        centrality_results, actual_network = self.analyze_network_centrality()
        
        print("\n=== ネットワーク中心性分析 ===")
        
        for centrality_type, values in centrality_results.items():
            print(f"\n{centrality_type.upper()} CENTRALITY:")
            sorted_agents = sorted(values.items(), key=lambda x: x[1], reverse=True)
            for agent_id, score in sorted_agents[:5]:  # トップ5を表示
                agent = self.agents[agent_id]
                print(f"  {agent_id} ({agent.role}): {score:.3f}")

    def draw_environment(self, filename="it_environment.png", ax=None, title=None):
        """環境を描画（役職情報付き）"""
        create_new_figure = (ax is None)
        if create_new_figure:
            plt.figure(figsize=(12, 10))
            ax = plt.gca()
        ax.clear()

        # ノードを役職別に色分け
        role_colors = {
            "CEO": "gold",
            "CTO": "orange", 
            "TechLead": "lightblue",
            "PM": "lightgreen",
            "Engineer": "lightcoral",
            "Designer": "plum"
        }

        # 基本グラフを描画
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edge_color='gray', width=1.0, alpha=0.8)

        # ノードを役職別に描画
        for node in self.G.nodes():
            role = self.role_mapping[node]
            color = role_colors.get(role, "lightgray")
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=[node], 
                                 node_color=color, node_size=600, ax=ax)

        # ノードラベル（ノード番号）
        nx.draw_networkx_labels(self.G, self.pos, ax=ax, font_size=8, font_color='black')

        # エージェントの位置を表示
        agent_positions = {}
        for agent in self.agents.values():
            if agent.position not in agent_positions:
                agent_positions[agent.position] = []
            agent_positions[agent.position].append(agent)

        # エージェントラベルを配置
        for node, agents_at_node in agent_positions.items():
            x, y = self.pos[node]
            for i, agent in enumerate(agents_at_node):
                offset_y = 0.15 * (i - len(agents_at_node)/2 + 0.5)
                ax.text(x, y + offset_y, agent.agent_id,
                       bbox=dict(facecolor='red', alpha=0.8),
                       horizontalalignment='center', fontsize=8, 
                       color='white', fontweight='bold')

        # 凡例を追加
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                     markerfacecolor=color, markersize=10, label=role)
                          for role, color in role_colors.items()]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

        ax.set_title(title if title else "IT Company Network", fontsize=14)
        ax.axis('off')

        if create_new_figure:
            plt.tight_layout()
            plt.savefig(filename, bbox_inches='tight')
            plt.close()
            print(f"✓ IT企業環境を {filename} に保存しました。")

    def _create_tree_layout(self):
        """平衡木グラフの階層レイアウトを手動で作成"""
        pos = {}
        depths = nx.single_source_shortest_path_length(self.G, 0)
        max_depth = max(depths.values())
        
        depth_groups = {}
        for node, depth in depths.items():
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(node)
        
        for depth in range(max_depth + 1):
            nodes_at_depth = depth_groups[depth]
            y = max_depth - depth
            
            if len(nodes_at_depth) == 1:
                x = 0
                pos[nodes_at_depth[0]] = (x, y)
            else:
                width = len(nodes_at_depth) - 1
                for i, node in enumerate(sorted(nodes_at_depth)):
                    x = (i - width/2) * 2
                    pos[node] = (x, y)
        
        return pos


# --- メイン実行部分 ---
if __name__ == "__main__":
    print("=== IT企業エージェントベースモデル ===")
    
    # 環境作成
    env = ITCompanyEnvironment(branches=2, height=3)
    
    # エージェントを配置
    env.add_agent("CEO_A", 0)  # CEOはルートノード
    env.add_agent("CTO_B", 1)  # CTOは第2層
    env.add_agent("ENG_C", 3)  # エンジニアは下層
    env.add_agent("ENG_D", 4)  # 別のエンジニア
    env.add_agent("PM_E", 2)   # PMは中間層
    
    # 初期状態を描画
    env.draw_environment(title="Initial IT Company Setup")
    
    # 情報カスケードのシミュレーション
    env.simulate_information_cascade("CEO_A", "新プロダクト戦略の変更", "strategic")
    env.simulate_information_cascade("CTO_B", "技術スタック変更の提案", "technical")
    
    # 中心性分析
    env.print_centrality_analysis()
    
    print("\n=== 情報伝達ログ ===")
    for log in env.information_flow_log:
        print(f"{log['from']} -> {log['to']}: {log['content'][:20]}... (コンテクスト: {log['context_remaining']:.2f})")