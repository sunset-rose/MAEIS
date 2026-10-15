import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.nn.utils.rnn import pad_sequence
import numpy as np, itertools, random, copy, math
from crazy_functions.emo_agent.txt_agent.model import SimpleAttention, MatchingAttention, Attention

# class RelationAttention(nn.Module):
#     def __init__(self, hidden_size):
#         super(RelationAttention, self).__init__()
#         self.query = nn.Linear(hidden_size, hidden_size)
#         self.key = nn.Linear(hidden_size, hidden_size)
#         self.value = nn.Linear(hidden_size, hidden_size)
#         self.score = nn.Linear(2 * hidden_size, 1)
#         self.gate = nn.Linear(hidden_size * 2, 1)
#
#     def forward(self, p, x, mask=None):
#         q = self.query(p)
#         k = self.key(x)
#         score = self.fuse(q, k)
#         if mask is not None:
#             mask = 1 - mask[:, None, :].expand(-1, score.size(1), -1)
#             score = score.masked_fill(mask == 1, -1e9)
#         score = F.softmax(score, 2)
#         v = self.value(x)
#         out = torch.einsum('bcl,bld->bcd', score, v) + p
#         g = self.gate(torch.cat([out, p], 2)).sigmoid()
#         out = g * out + (1 - g) * p
#         return out
#
#     def fuse(self, x, y):
#         x = x.unsqueeze(2).expand(-1, -1, y.size(1), -1)
#         y = y.unsqueeze(1).expand(-1, x.size(1), -1, -1)
#         temp = torch.cat([x, y], 3)
#         return self.score(temp).squeeze(3)
#
# import gc
# class GATLayer(nn.Module):
#
#     def __init__(self, D_m):
#         super().__init__()
#         D_m = 768
#         # self.ura3 = TypeAttention(D_m)
#         # self.x1ra3 = TypeAttention(D_m)
#         # self.x2ra3 = TypeAttention(D_m)
#         # self.x3ra3 = TypeAttention(D_m)
#         # self.o1ra3 = TypeAttention(D_m)
#         # self.o2ra3 = TypeAttention(D_m)
#
#         # self.ux1 = RelationAttention(D_m)
#         # self.ux2 = RelationAttention(D_m)
#         # self.ux3 = RelationAttention(D_m)
#         # self.uo1 = RelationAttention(D_m)
#         # self.uo2 = RelationAttention(D_m)
#         #
#         # self.x1u = RelationAttention(D_m)
#         self.x12 = RelationAttention(D_m)
#         self.x13 = RelationAttention(D_m)
#         self.xo11 = RelationAttention(D_m)
#         self.xo12 = RelationAttention(D_m)
#
#         # self.x2u = RelationAttention(D_m)
#         self.x21 = RelationAttention(D_m)
#         self.x23 = RelationAttention(D_m)
#         self.xo21 = RelationAttention(D_m)
#         self.xo22 = RelationAttention(D_m)
#
#         # self.x3u = RelationAttention(D_m)
#         self.x31 = RelationAttention(D_m)
#         self.x32 = RelationAttention(D_m)
#         self.xo31 = RelationAttention(D_m)
#         self.xo32 = RelationAttention(D_m)
#
#         # self.o1u = RelationAttention(D_m)
#         self.ox11 = RelationAttention(D_m)
#         self.ox12 = RelationAttention(D_m)
#         self.ox13 = RelationAttention(D_m)
#         self.o12 = RelationAttention(D_m)
#
#         # self.o2u = RelationAttention(D_m)
#         self.ox21 = RelationAttention(D_m)
#         self.ox22 = RelationAttention(D_m)
#         self.ox23 = RelationAttention(D_m)
#         self.o21 = RelationAttention(D_m)
#
#         self.Dm = D_m
#
#     def forward(self, u, x1, x2, x3, o1, o2, mask=None):
#
#         # # [sq,bs,hd]
#         # u_avg = torch.transpose(u, 0, 1)
#         # # [bs,hd]
#         # u_avg = torch.mean(u_avg, 0)
#         # u_avg = u_avg.unsqueeze(1)
#         #
#         # x1_avg = torch.transpose(x1, 0, 1)
#         # x1_avg = torch.mean(x1_avg, 0)
#         # x1_avg = x1_avg.unsqueeze(1)
#         #
#         # x2_avg = torch.transpose(x2, 0, 1)
#         # x2_avg = torch.mean(x2_avg, 0)
#         # x2_avg = x2_avg.unsqueeze(1)
#         #
#         # x3_avg = torch.transpose(x3, 0, 1)
#         # x3_avg = torch.mean(x3_avg, 0)
#         # x3_avg = x3_avg.unsqueeze(1)
#         #
#         # o1_avg = torch.transpose(o1, 0, 1)
#         # o1_avg = torch.mean(o1_avg, 0)
#         # o1_avg = o1_avg.unsqueeze(1)
#         #
#         # o2_avg = torch.transpose(o2, 0, 1)
#         # o2_avg = torch.mean(o2_avg, 0)
#         # o2_avg = o2_avg.unsqueeze(1)
#         #
#         # # u_avg = u.mean(dim=1)
#         # # x1_avg = x1.mean(dim=1)
#         # # x2_avg = x2.mean(dim=1)
#         # # x3_avg = x3.mean(dim=1)
#         # # o1_avg = o1.mean(dim=1)
#         # # o2_avg = o2.mean(dim=1)
#         #
#         # # u_avg = u_avg.unsqueeze(1)
#         # # x1_avg = x1_avg.unsqueeze(1)
#         # # x2_avg = x2_avg.unsqueeze(1)
#         # # x3_avg = x3_avg.unsqueeze(1)
#         # # o1_avg = o1_avg.unsqueeze(1)
#         # # o2_avg = o2_avg.unsqueeze(1)
#         #
#         # u_avg1 = torch.cat((x1_avg, x2_avg, x3_avg, o1_avg, o2_avg), dim=1)
#         # x1_avg1 = torch.cat((u_avg, x2_avg, x3_avg, o1_avg, o2_avg), dim=1)
#         # x2_avg1 = torch.cat((u_avg, x1_avg, x3_avg, o1_avg, o2_avg), dim=1)
#         # x3_avg1 = torch.cat((u_avg, x1_avg, x2_avg, o1_avg, o2_avg), dim=1)
#         # o1_avg1 = torch.cat((u_avg, x1_avg, x2_avg, x3_avg, o2_avg), dim=1)
#         # o2_avg1 = torch.cat((u_avg, x1_avg, x2_avg, x3_avg, o1_avg), dim=1)
#         #
#         # # # [bs,5,Dm]
#         # # u_avg1 = u_avg1.unsqueeze(2).expand(-1, -1, self.Dm)
#         # # x1_avg1 = x1_avg1.unsqueeze(2).expand(-1, -1, self.Dm)
#         # # x2_avg1 = x2_avg1.unsqueeze(2).expand(-1, -1, self.Dm)
#         # # x3_avg1 = x3_avg1.unsqueeze(2).expand(-1, -1, self.Dm)
#         # # o1_avg1 = o1_avg1.unsqueeze(2).expand(-1, -1, self.Dm)
#         # # o2_avg1 = o2_avg1.unsqueeze(2).expand(-1, -1, self.Dm)
#         # #
#         # # # [bs,1,Dm]
#         # # u1 = u.unsqueeze(1)
#         # # x11 = x1.unsqueeze(1)
#         # # x21 = x2.unsqueeze(1)
#         # # x31 = x3.unsqueeze(1)
#         # # o11 = o1.unsqueeze(1)
#         # # o21 = o2.unsqueeze(1)
#         #
#         # u_type = self.ura3(u, u_avg1)
#         # x1_type = self.x1ra3(x1, x1_avg1)
#         # x2_type = self.x2ra3(x2, x2_avg1)
#         # x3_type = self.x3ra3(x3, x3_avg1)
#         # o1_type = self.o1ra3(o1, o1_avg1)
#         # o2_type = self.o2ra3(o2, o2_avg1)
#
#         # u_x1 = self.ux1(u, x1)
#         # u_x2 = self.ux2(u, x2)
#         # u_x3 = self.ux3(u, x3)
#         # u_o1 = self.uo1(u, o1)
#         # u_o2 = self.uo2(u, o2)
#         # # u = u + u_x1 + u_x2 + u_x3 + u_o1 + u_o2 + u_type
#         # u = u + u_x1 + u_x2 + u_x3 + u_o1 + u_o2
#
#         # x1_u = self.x1u(x1, u)
#         x1_x2 = self.x12(x1, x2)
#         x1_x3 = self.x13(x1, x3)
#         x1_o1 = self.xo11(x1, o1)
#         x1_o2 = self.xo12(x1, o2)
#         # x1 = x1 + x1_u + x1_x2 + x1_x3 + x1_o1 + x1_o2 + x1_type
#         x1 = x1 + x1_x2 + x1_x3 + x1_o1 + x1_o2
#
#         # x2_u = self.x2u(x2, u)
#         x2_x1 = self.x21(x2, x1)
#         x2_x3 = self.x23(x2, x3)
#         x2_o1 = self.xo21(x2, o1)
#         x2_o2 = self.xo22(x2, o2)
#         # x2 = x1 + x2_u + x2_x1 + x2_x3 + x2_o1 + x2_o2 + x2_type
#         x2 = x1 + x2_x1 + x2_x3 + x2_o1 + x2_o2
#
#         # x3_u = self.x2u(x3, u)
#         x3_x1 = self.x31(x3, x1)
#         x3_x2 = self.x32(x3, x2)
#         x3_o1 = self.xo31(x3, o1)
#         x3_o2 = self.xo32(x3, o2)
#         # x3 = x3 + x3_u + x3_x1 + x3_x2 + x3_o1 + x3_o2 + x3_type
#         x3 = x3 + x3_x1 + x3_x2 + x3_o1 + x3_o2
#
#         # o1_u = self.o1u(o1, u)
#         o1_x1 = self.ox11(o1, x1)
#         o1_x2 = self.ox12(o1, x2)
#         o1_x3 = self.ox13(o1, x3)
#         o1_o2 = self.o12(o1, o2)
#         # o1 = o1 + o1_u + o1_x1 + o1_x3 + o1_x2 + o1_o2 + o1_type
#         o1 = o1 + o1_x1 + o1_x3 + o1_x2 + o1_o2
#
#         # o2_u = self.o2u(o2, u)
#         o2_x1 = self.ox21(o2, x1)
#         o2_x2 = self.ox22(o2, x2)
#         o2_x3 = self.ox23(o2, x3)
#         o2_o1 = self.o21(o2, o1)
#         # o2 = o2 + o2_u + o2_x1 + o2_x3 + o2_x2 + o2_o1 + o2_type
#         o2 = o2 + o2_x1 + o2_x3 + o2_x2 + o2_o1
#
#         return u, x1, x2, x3, o1, o2

class CommonsenseRNNCell(nn.Module):

    def __init__(self, D_m, D_s, D_g, D_p, D_r, D_i, D_e, listener_state=False,
                 context_attention='simple', D_a=100, dropout=0.5, emo_gru=True):
        super(CommonsenseRNNCell, self).__init__()

        self.D_m = D_m
        self.D_s = D_s
        self.D_g = D_g
        self.D_p = D_p
        self.D_r = D_r
        self.D_i = D_i
        self.D_e = D_e

        # print ('dmsg', D_m, D_s, D_g)
        self.g_cell = nn.GRUCell(D_m+D_p+D_r, D_g)
        self.p_cell = nn.GRUCell(D_s+D_g, D_p)
        self.r_cell = nn.GRUCell(D_m+D_s+D_g, D_r)
        self.i_cell = nn.GRUCell(D_s+D_p, D_i)
        self.e_cell = nn.GRUCell(D_m+D_p+D_r+D_i, D_e)


        self.emo_gru = emo_gru
        self.listener_state = listener_state
        if listener_state:
            self.pl_cell = nn.GRUCell(D_s+D_g, D_p)
            self.rl_cell = nn.GRUCell(D_m+D_s+D_g, D_r)

        self.dropout = nn.Dropout(dropout)

        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)
        self.dropout4 = nn.Dropout(dropout)
        self.dropout5 = nn.Dropout(dropout)

        if context_attention=='simple':
            self.attention = SimpleAttention(D_g)
        else:
            self.attention = MatchingAttention(D_g, D_m, D_a, context_attention)


        # self.layers = nn.ModuleList([GATLayer(D_m) for _ in range(1)])
        # # U
        # self.U_embed = nn.Embedding(8, D_s)
        # self.U_linear = nn.Linear(D_s, D_s)
        # # x1
        # self.x1_embed = nn.Embedding(8, D_s)
        # self.x1_linear = nn.Linear(D_s, D_s)
        # # x2
        # self.x2_embed = nn.Embedding(8, D_s)
        # self.x2_linear = nn.Linear(D_s, D_s)
        # # x3
        # self.x3_embed = nn.Embedding(8, D_s)
        # self.x3_linear = nn.Linear(D_s, D_s)
        # # o1
        # self.o1_embed = nn.Embedding(8, D_s)
        # self.o1_linear = nn.Linear(D_s, D_s)
        # # o2
        # self.o2_embed = nn.Embedding(8, D_s)
        # self.o2_linear = nn.Linear(D_s, D_s)

    def _select_parties(self, X, indices):
        q0_sel = []
        for idx, j in zip(indices, X):
            q0_sel.append(j[idx].unsqueeze(0))
        q0_sel = torch.cat(q0_sel,0)
        return q0_sel

    # def gat_layer(self, U, x1, x2, x3, o1, o2, mask=None):
    #     for m in self.layers:
    #         U, x1, x2, x3, o1, o2 = m(U, x1, x2, x3, o1, o2, mask)
    #     return U, x1, x2, x3, o1, o2

    def forward(self, U, x1, x2, x3, o1, o2, qmask, g_hist, q0, r0, i0, e0):
        """
        U -> batch, D_m
        x1, x2, x3, o1, o2 -> batch, D_m
        x1 -> effect on self; x2 -> reaction of self; x3 -> intent of self
        o1 -> effect on others; o2 -> reaction of others
        qmask -> batch, party
        g_hist -> t-1, batch, D_g
        q0 -> batch, party, D_p
        e0 -> batch, self.D_e
        """
        qm_idx = torch.argmax(qmask, 1)
        q0_sel = self._select_parties(q0, qm_idx)
        r0_sel = self._select_parties(r0, qm_idx)

        #处理维度
        # U1 = U.unsqueeze(2).expand(-1, -1, 768)
        # x11 = x1.unsqueeze(1).expand(-1, 100, -1)
        # x21 = x2.unsqueeze(1).expand(-1, 100, -1)
        # x31 = x3.unsqueeze(1).expand(-1, 100, -1)
        # o11 = o1.unsqueeze(1).expand(-1, 100, -1)
        # o21 = o2.unsqueeze(1).expand(-1, 100, -1)
        #
        # # 加gat层
        # U2, x12, x22, x32, o12, o22 = self.gat_layer(U1, x11, x21, x31, o11, o21, qmask)
        # gc.collect()
        # torch.cuda.empty_cache()
        #
        # U3 = U2.mean(dim=2)
        # x13 = x12.mean(dim=1)
        # x23 = x22.mean(dim=1)
        # x33 = x32.mean(dim=1)
        # o13 = o12.mean(dim=1)
        # o23 = o22.mean(dim=1)
        #
        # U = U3
        # x1 = x13
        # x2 = x23
        # x3 = x33
        # o1 = o13
        # o2 = o23

        ## global state ##
        g_ = self.g_cell(torch.cat([U, q0_sel, r0_sel], dim=1),
                         torch.zeros(U.size()[0],self.D_g).type(U.type()) if g_hist.size()[0]==0 else
                         g_hist[-1])
        # g_ = self.dropout(g_)

        ## context ##
        if g_hist.size()[0]==0:
            c_ = torch.zeros(U.size()[0], self.D_g).type(U.type())
            alpha = None
        else:
            c_, alpha = self.attention(g_hist, U)

        ## external state ##
        U_r_c_ = torch.cat([U, x2, c_], dim=1).unsqueeze(1).expand(-1, qmask.size()[1],-1)
        # print ('urc', U_r_c_.size())
        # print ('u x2, c', U.size(), x2.size(), c_.size())
        rs_ = self.r_cell(U_r_c_.contiguous().view(-1, self.D_m+self.D_s+self.D_g),
                          r0.view(-1, self.D_r)).view(U.size()[0], -1, self.D_r)
        # rs_ = self.dropout(rs_)

        ## internal state ##
        es_c_ = torch.cat([x1, c_], dim=1).unsqueeze(1).expand(-1,qmask.size()[1],-1)
        qs_ = self.p_cell(es_c_.contiguous().view(-1, self.D_s+self.D_g),
                          q0.view(-1, self.D_p)).view(U.size()[0], -1, self.D_p)
        # qs_ = self.dropout(qs_)


        if self.listener_state:
            ## listener external state ##
            U_ = U.unsqueeze(1).expand(-1,qmask.size()[1],-1).contiguous().view(-1,self.D_m)
            er_ = o2.unsqueeze(1).expand(-1, qmask.size()[1], -1).contiguous().view(-1, self.D_s)
            ss_ = self._select_parties(rs_, qm_idx).unsqueeze(1). \
                expand(-1, qmask.size()[1], -1).contiguous().view(-1, self.D_r)
            U_er_ss_ = torch.cat([U_, er_, ss_], 1)
            rl_ = self.rl_cell(U_er_ss_, r0.view(-1, self.D_r)).view(U.size()[0], -1, self.D_r)
            # rl_ = self.dropout(rl_)

            ## listener internal state ##
            es_ = o1.unsqueeze(1).expand(-1, qmask.size()[1], -1).contiguous().view(-1, self.D_s)
            ss_ = self._select_parties(qs_, qm_idx).unsqueeze(1). \
                expand(-1, qmask.size()[1], -1).contiguous().view(-1, self.D_p)
            es_ss_ = torch.cat([es_, ss_], 1)
            ql_ = self.pl_cell(es_ss_, q0.view(-1, self.D_p)).view(U.size()[0], -1, self.D_p)
            # ql_ = self.dropout(ql_)

        else:
            rl_ = r0
            ql_ = q0

        qmask_ = qmask.unsqueeze(2)
        q_ = ql_*(1-qmask_) + qs_*qmask_
        r_ = rl_*(1-qmask_) + rs_*qmask_

        ## intent ##
        i_q_ = torch.cat([x3, self._select_parties(q_, qm_idx)], dim=1).unsqueeze(1).expand(-1, qmask.size()[1], -1)
        is_ = self.i_cell(i_q_.contiguous().view(-1, self.D_s+self.D_p),
                          i0.view(-1, self.D_i)).view(U.size()[0], -1, self.D_i)
        # is_ = self.dropout(is_)
        il_ = i0
        i_ = il_*(1-qmask_) + is_*qmask_

        ## emotion ##
        es_ = torch.cat([U, self._select_parties(q_, qm_idx), self._select_parties(r_, qm_idx),
                         self._select_parties(i_, qm_idx)], dim=1)
        e0 = torch.zeros(qmask.size()[0], self.D_e).type(U.type()) if e0.size()[0]==0 \
            else e0

        if self.emo_gru:
            e_ = self.e_cell(es_, e0)
        else:
            e_ = es_

            # e_ = self.dropout(e_)
        g_ = self.dropout1(g_)
        q_ = self.dropout2(q_)
        r_ = self.dropout3(r_)
        i_ = self.dropout4(i_)
        e_ = self.dropout5(e_)

        return g_, q_, r_, i_, e_, alpha


class CommonsenseRNN(nn.Module):

    def __init__(self, D_m, D_s, D_g, D_p, D_r, D_i, D_e, listener_state=False,
                            context_attention='simple', D_a=100, dropout=0.5, emo_gru=True):
        super(CommonsenseRNN, self).__init__()

        self.D_m = D_m
        self.D_g = D_g
        self.D_p = D_p
        self.D_r = D_r
        self.D_i = D_i
        self.D_e = D_e
        self.dropout = nn.Dropout(dropout)

        self.dialogue_cell = CommonsenseRNNCell(D_m, D_s, D_g, D_p, D_r, D_i, D_e,
                            listener_state, context_attention, D_a, dropout, emo_gru)

    #     self.layers = nn.ModuleList([GATLayer(D_m) for _ in range(2)])
    # def gat_layer(self, U, x1, x2, x3, o1, o2, mask=None):
    #     for m in self.layers:
    #         U, x1, x2, x3, o1, o2 = m(U, x1, x2, x3, o1, o2, mask)
    #     return U, x1, x2, x3, o1, o2


    def forward(self, U, x1, x2, x3, o1, o2, qmask):
        """
        U -> seq_len, batch, D_m
        x1, x2, x3, o1, o2 -> seq_len, batch, D_s
        qmask -> seq_len, batch, party
        """
        # # batch, seq_len, D_m
        # U1 = torch.transpose(U, 0, 1)
        # # batch, seq_len, D_s
        # x11 = torch.transpose(x1, 0, 1)
        # x21 = torch.transpose(x2, 0, 1)
        # x31 = torch.transpose(x3, 0, 1)
        # o11 = torch.transpose(o1, 0, 1)
        # o21 = torch.transpose(o2, 0, 1)
        #
        # # 加gat层
        # U2, x12, x22, x32, o12, o22 = self.gat_layer(U1, x11, x21, x31, o11, o21, qmask)
        # # gc.collect()
        # # torch.cuda.empty_cache()
        #
        # # U1 = torch.transpose(U2, 0, 1)
        # # batch, seq_len, D_s
        # x1 = torch.transpose(x12, 0, 1)
        # x2 = torch.transpose(x22, 0, 1)
        # x3 = torch.transpose(x32, 0, 1)
        # o1 = torch.transpose(o12, 0, 1)
        # o2 = torch.transpose(o22, 0, 1)

        g_hist = torch.zeros(0).type(U.type()) # 0-dimensional tensor
        q_ = torch.zeros(qmask.size()[1], qmask.size()[2], self.D_p).type(U.type()) # batch, party, D_p
        r_ = torch.zeros(qmask.size()[1], qmask.size()[2], self.D_r).type(U.type()) # batch, party, D_r
        i_ = torch.zeros(qmask.size()[1], qmask.size()[2], self.D_i).type(U.type()) # batch, party, D_i

        e_ = torch.zeros(0).type(U.type()) # batch, D_e
        e = e_

        alpha = []
        for u_, x1_, x2_, x3_, o1_, o2_, qmask_ in zip(U, x1, x2, x3, o1, o2, qmask):

            g_, q_, r_, i_, e_, alpha_ = self.dialogue_cell(u_, x1_, x2_, x3_, o1_, o2_,
                                                            qmask_, g_hist, q_, r_, i_, e_)

            g_hist = torch.cat([g_hist, g_.unsqueeze(0)],0)
            e = torch.cat([e, e_.unsqueeze(0)],0)

            if type(alpha_)!=type(None):
                alpha.append(alpha_[:,0,:])

        return e, alpha # seq_len, batch, D_e


class CommonsenseGRUModel(nn.Module):

    def __init__(self, D_m, D_s, D_g, D_p, D_r, D_i, D_e, D_h, D_a=100, n_classes=7, listener_state=False,
        context_attention='simple', dropout_rec=0.5, dropout=0.1, emo_gru=True, mode1=0, norm=0, residual=False):

        super(CommonsenseGRUModel, self).__init__()

        if mode1 == 0:
            D_x = 4 * D_m
        elif mode1 == 1:
            D_x = 2 * D_m
        else:
            D_x = D_m

        self.mode1 = mode1
        self.norm_strategy = norm
        self.linear_in = nn.Linear(D_x, D_h)
        self.residual = residual

        self.r_weights = nn.Parameter(torch.tensor([0.25, 0.25, 0.25, 0.25]))

        norm_train = True
        self.norm1a = nn.LayerNorm(D_m, elementwise_affine=norm_train)
        self.norm1b = nn.LayerNorm(D_m, elementwise_affine=norm_train)
        self.norm1c = nn.LayerNorm(D_m, elementwise_affine=norm_train)
        self.norm1d = nn.LayerNorm(D_m, elementwise_affine=norm_train)

        self.norm3a = nn.BatchNorm1d(D_m, affine=norm_train)
        self.norm3b = nn.BatchNorm1d(D_m, affine=norm_train)
        self.norm3c = nn.BatchNorm1d(D_m, affine=norm_train)
        self.norm3d = nn.BatchNorm1d(D_m, affine=norm_train)

        self.dropout   = nn.Dropout(dropout)
        self.dropout_rec = nn.Dropout(dropout_rec)
        self.cs_rnn_f = CommonsenseRNN(D_h, D_s, D_g, D_p, D_r, D_i, D_e, listener_state,
                                       context_attention, D_a, dropout_rec, emo_gru)
        self.cs_rnn_r = CommonsenseRNN(D_h, D_s, D_g, D_p, D_r, D_i, D_e, listener_state,
                                       context_attention, D_a, dropout_rec, emo_gru)
        self.sense_gru = nn.GRU(input_size=D_s, hidden_size=D_s//2, num_layers=1, bidirectional=True)
        self.matchatt = MatchingAttention(2*D_e,2*D_e,att_type='general2')
        self.linear     = nn.Linear(2*D_e, D_h)
        self.smax_fc    = nn.Linear(D_h, n_classes)

    def _reverse_seq(self, X, mask):
        """
        X -> seq_len, batch, dim
        mask -> batch, seq_len
        """
        X_ = X.transpose(0,1)
        mask_sum = torch.sum(mask, 1).int()

        xfs = []
        for x, c in zip(X_, mask_sum):
            xf = torch.flip(x[:c], [0])
            xfs.append(xf)
        return pad_sequence(xfs)

    def forward(self, r1, r2, r3, r4, x1, x2, x3, o1, o2, qmask, umask, att2=False, return_hidden=False):
        """
        U -> seq_len, batch, D_m
        qmask -> seq_len, batch, party
        """

        seq_len, batch, feature_dim = r1.size()

        if self.norm_strategy == 1:
            r1 = self.norm1a(r1.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)
            r2 = self.norm1b(r2.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)
            r3 = self.norm1c(r3.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)
            r4 = self.norm1d(r4.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)

        elif self.norm_strategy == 2:
            norm2 = nn.LayerNorm((seq_len, feature_dim), elementwise_affine=False)
            r1 = norm2(r1.transpose(0, 1)).transpose(0, 1)
            r2 = norm2(r2.transpose(0, 1)).transpose(0, 1)
            r3 = norm2(r3.transpose(0, 1)).transpose(0, 1)
            r4 = norm2(r4.transpose(0, 1)).transpose(0, 1)

        elif self.norm_strategy == 3:
            r1 = self.norm3a(r1.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)
            r2 = self.norm3b(r2.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)
            r3 = self.norm3c(r3.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)
            r4 = self.norm3d(r4.transpose(0, 1).reshape(-1, feature_dim)).reshape(-1, seq_len, feature_dim).transpose(1, 0)

        if self.mode1 == 0:
            r = torch.cat([r1, r2, r3, r4], axis=-1)
        elif self.mode1 == 1:
            r = torch.cat([r1, r2], axis=-1)
        elif self.mode1 == 2:
            r = (r1 + r2 + r3 + r4)/4
        elif self.mode1 == 3:
            r = r1
        elif self.mode1 == 4:
            r = r2
        elif self.mode1 == 5:
            r = r3
        elif self.mode1 == 6:
            r = r4
        elif self.mode1 == 7:
            r = self.r_weights[0]*r1 + self.r_weights[1]*r2 + self.r_weights[2]*r3 + self.r_weights[3]*r4

        r = self.linear_in(r)

        emotions_f, alpha_f = self.cs_rnn_f(r, x1, x2, x3, o1, o2, qmask)

        out_sense, _ = self.sense_gru(x1)

        rev_r = self._reverse_seq(r, umask)
        rev_x1 = self._reverse_seq(x1, umask)
        rev_x2 = self._reverse_seq(x2, umask)
        rev_x3 = self._reverse_seq(x3, umask)
        rev_o1 = self._reverse_seq(o1, umask)
        rev_o2 = self._reverse_seq(o2, umask)
        rev_qmask = self._reverse_seq(qmask, umask)
        emotions_b, alpha_b = self.cs_rnn_r(rev_r, rev_x1, rev_x2, rev_x3, rev_o1, rev_o2, rev_qmask)
        emotions_b = self._reverse_seq(emotions_b, umask)

        emotions = torch.cat([emotions_f,emotions_b],dim=-1)
        emotions = self.dropout_rec(emotions)

        alpha, alpha_f, alpha_b = [], [], []
        if att2:
            att_emotions = []
            alpha = []
            for t in emotions:
                att_em, alpha_ = self.matchatt(emotions,t,mask=umask)
                att_emotions.append(att_em.unsqueeze(0))
                alpha.append(alpha_[:,0,:])
            att_emotions = torch.cat(att_emotions,dim=0)
            hidden = F.relu(self.linear(att_emotions))
        else:
            hidden = F.relu(self.linear(emotions))

        hidden = self.dropout(hidden)

        if self.residual:
            hidden = hidden + r

        log_prob = F.log_softmax(self.smax_fc(hidden), 2)

        if return_hidden:
            return hidden, alpha, alpha_f, alpha_b, emotions
        return log_prob, out_sense, alpha, alpha_f, alpha_b, emotions
    
    