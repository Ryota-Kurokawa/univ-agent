import networkx as nx
import matplotlib.pyplot as plt
import random

# ★修正点: pydotの有無をチェックし、なければspring_layoutに切り替える
try:
    # 実際に内部で使われるpydotをインポートできるか試す
    import pydot
    from networkx.drawing.nx_pydot import graphviz_layout
    LAYOUT_ENGINE = "graphviz"
    print("✓ pydotライブラリが見つかりました。階層レイアウトを使用します。")
except ImportError:
    LAYOUT_ENGINE = "spring"
    print("警告: 'pydot'またはGraphviz本体が見つかりません。代替のspring_layoutで描画します。")
    print("      綺麗な階層レイアウトを使用するには、Graphvizとpydotをインストールしてください。")
    print("      (ターミナルで `brew install graphviz` と `pip install pydot` を実行)")


class Agent:
    """
    エージェントを定義するクラス。
    """
    def __init__(self, agent_id, initial_node, initial_info=None):
        """
        エージェントを初期化する。
        - agent_id: エージェントのユニークなID (例: "A1")
        - initial_node: エージェントの初期配置ノード。
        - initial_info: エージェントが最初に持っている情報
        """
        self.agent_id = agent_id
        self.position = initial_node
        self.information = {initial_info} if initial_info else set()
        print(f"エージェント {self.agent_id} が生成されました。初期位置: {self.position}")


class Environment:
    """
    エージェントが活動する環境を定義するクラス。
    グラフ構造やエージェントの管理を行う。
    """
    def __init__(self, branches=2, height=3):
        """
        環境を初期化する。
        - branches (r): 各ノードの分岐数
        - height (h): 木の階層の深さ
        """
        self.G = nx.balanced_tree(branches, height)
        self.agents = {}
        
        # ★修正点: LAYOUT_ENGINEの値に応じてレイアウト方法を決定
        if LAYOUT_ENGINE == "graphviz":
            self.pos = graphviz_layout(self.G, prog='twopi', root=0)
        else:
            self.pos = nx.spring_layout(self.G, seed=42, iterations=100)

        total_nodes = len(self.G.nodes)
        print(f"平衡木グラフ環境が生成されました (分岐数:{branches}, 高さ:{height}, 総ノード数:{total_nodes})。")

    def add_agent(self, agent_id, start_node, initial_info=None):
        if start_node not in self.G.nodes():
            print(f"エラー: ノード {start_node} は環境内に存在しません。")
            return None
        agent = Agent(agent_id, start_node, initial_info)
        self.agents[agent_id] = agent
        print(f"エージェント {agent_id} がノード {start_node} に配置されました。")
        return agent

    def draw_environment(self, filename="environment.png"):
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        
        # ★修正点: レイアウトによって文字の位置を微調整
        label_offset = 20 if LAYOUT_ENGINE == "graphviz" else 0.05

        nx.draw_networkx_nodes(self.G, self.pos, node_color='lightgreen', node_size=400)
        nx.draw_networkx_edges(self.G, self.pos, edge_color='gray', width=1.0, alpha=0.8)
        nx.draw_networkx_labels(self.G, self.pos, font_size=8, font_color='black')

        agent_positions = {agent.agent_id: agent.position for agent in self.agents.values()}
        agent_nodes = list(agent_positions.values())

        nx.draw_networkx_nodes(self.G, self.pos, nodelist=agent_nodes, node_color='tomato', node_size=500)
        
        for agent_id, node in agent_positions.items():
            x, y = self.pos[node]
            plt.text(x, y + label_offset, s=agent_id,
                     bbox=dict(facecolor='tomato', alpha=0.8),
                     horizontalalignment='center',
                     fontsize=9,
                     color='white',
                     fontweight='bold')

        plt.title("Environment State (Tree Structure)", fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        print(f"✓ 環境の状態を {filename} に保存しました。")


# --- メインの処理 ---
if __name__ == "__main__":
    print("--- シミュレーション設定 ---")
    env = Environment(branches=2, height=3)

    agent1 = env.add_agent("A1", 0, "情報_アルファ")
    outer_nodes = [node for node, degree in env.G.degree() if degree == 1]
    if outer_nodes:
      agent2 = env.add_agent("B2", random.choice(outer_nodes), "情報_ベータ")

    env.draw_environment("initial_state_tree.png")

    simulation_steps = 5
    print(f"\n--- {simulation_steps}ステップのシミュレーション開始 ---")

    for i in range(simulation_steps):
        print(f"\n--- ステップ {i+1} ---")
        for agent_id, agent in env.agents.items():
            neighbors = list(env.G.neighbors(agent.position))
            if neighbors:
                new_position = random.choice(neighbors)
                agent.position = new_position
                print(f"エージェント {agent_id} がノード {new_position} に移動しました。")

        env.draw_environment(f"step_{i+1}_tree.png")

    print("\n--- シミュレーション完了 ---")